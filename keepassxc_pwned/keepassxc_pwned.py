#!/usr/bin/env python3

"""Check a keepassxc database against previously cracked haveibeenpwned passwords

Usage:
    keepassxc_pwned [--help]
    keepassxc_pwned <KDBX_DATABASE_FILE> [--plaintext] [--no-logs]

Options:
    KDBX_DATABASE_FILE      The path to your keepassxc database file
    --plaintext             Print breached passwords in plaintext; defaults to sha1 hashes
    --no-logs               Don't print status messages, just the summary message

Examples:
    keepassxc_pwned ~/database.kdbx
    keepassxc_pwned ~/database.kdbx --plaintext
"""

import sys
import os
import time
import logging
import shlex
import getpass
import subprocess
import xml.etree.cElementTree as ET
from dataclasses import dataclass
from typing import List
from distutils.version import StrictVersion

import docopt

from keepassxc_pwned.password import lookup_pwned

args = docopt.docopt(__doc__)
kdbx_db_location = args["<KDBX_DATABASE_FILE>"]
if kdbx_db_location is None:
    print("Error: You didn't provide a database file to check!", file=sys.stderr)
    print(__doc__)
    sys.exit(1)
print_plaintext = args["--plaintext"]
log_level = logging.ERROR if args["--no-logs"] else logging.INFO
logger = logging.getLogger("keepassxc_pwned_logger")
sh = logging.StreamHandler(sys.stdout)
sh.setLevel(log_level)
logging.getLogger().setLevel(log_level)  # https://stackoverflow.com/questions/32681289
sh.setFormatter(logging.Formatter("%(msg)s"))
logger.addHandler(sh)


@dataclass(init=False, repr=False)
class Credential:
    username: str
    password: str
    title: str
    sha1: str
    count: int  # occurences on haveibeenpwned

    def __repr__(self):
        valid_attrs = []
        for attr in ["title", "username", "password", "sha1", "count"]:
            if hasattr(self, attr):
                valid_attrs.append("{}={}".format(attr, repr(getattr(self, attr))))
        return "{}({})".format(self.__class__.__name__, ", ".join(valid_attrs))

    __str__ = __repr__

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        try:
            return (
                self.title == other.title
                and self.username == other.username
                and self.password == other.password
            )
        except AttributeError:
            return self.password == other.password

    def display(self):
        """An basic representation of this credential"""
        if self.title:
            return self.title
        elif self.username:
            return self.username
        else:
            return self.password


def verify_binary_exists():
    """Make sure the keepassxc-cli binary exists"""
    shell_output = subprocess.run(["which", "keepassxc-cli"], capture_output=True)
    if shell_output.returncode != 0:
        logger.critical(
            "Could not find the keepassxc-cli binary. Verify its installed and on your $PATH."
        )
        sys.exit(1)


def backwards_compatible_export() -> str:
    """
    In KeepassXC version 2.5.0, the extract command was re-named to export
    Attempt to parse the version number and generate the correct subcommand
    """
    version_proc = subprocess.run(
        shlex.split("keepassxc-cli --version"),
        encoding='utf-8',
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    version = version_proc.stdout.strip()
    try:
        if StrictVersion(version) < StrictVersion('2.5.0'):
            return 'extract'
        else:
            return 'export'
    except ValueError:  # could not parse version number
        return "export"

def parse_keepassxc_cli_xml(kdbx_location) -> List[Credential]:
    """Call the keepassxc-cli binary and extract the title, usernames and passwords"""

    keepassxc_cli_subcommand = backwards_compatible_export()
    credentials = []
    # use command line binary to passwords from kdbx in XML
    command = "keepassxc-cli {} {}".format(keepassxc_cli_subcommand, kdbx_location)
    password = getpass.getpass("Insert password for {}: ".format(kdbx_location))
    keepassxc_output = subprocess.run(
        shlex.split(command),
        input=password,
        encoding="utf-8",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if keepassxc_output.returncode != 0:
        logger.critical(keepassxc_output.stderr)
        sys.exit(1)
    # python doesnt like the version tag, remove the first line
    keepass_xml_str = keepassxc_output.stdout.split(os.linesep, 2)[-1]
    password_xml_tree = ET.fromstring(text=keepass_xml_str)
    for group in password_xml_tree.find("Root").iter("Group"):
        # ignore deleted passwords
        if group.find("Name").text == "Recycle Bin":
            continue
        # grab username, title, and passwords
        for entry in filter(lambda g: g.tag == "Entry", group.getchildren()):
            c = Credential()
            for str_node in filter(lambda e: e.tag == "String", entry.getchildren()):
                key = str_node.find("Key").text
                value = str_node.find("Value").text
                if key == "Title":
                    c.title = value
                elif key == "UserName":
                    c.username = value
                elif key == "Password":
                    c.password = value
            if c.password is not None:
                if c not in credentials:
                    credentials.append(c)
            else:
                pass
                # There seem to be duplicates for entries that dont include passwords, ignore them
                # logger.warning(f"No password for {c.display()}")
    credentials.sort(key=lambda c: c.display().lower())
    return credentials


def main():
    if not os.path.exists(kdbx_db_location):
        logger.critical("Could not find a file at {}".format(kdbx_db_location))
        sys.exit(1)
    verify_binary_exists()  # make sure keepassxc-cli exists
    credentials: List[Credential] = parse_keepassxc_cli_xml(kdbx_db_location)
    breached_passwords = []
    for c in credentials:
        logger.info(f"Checking password for {c.display()}...")
        sha1, count = lookup_pwned(c.password, logger)
        time.sleep(2)
        if count != 0:
            logger.info(
                "Found password for '{}' {} times in the dataset!".format(
                    c.display(), count
                )
            )
            c.sha1 = sha1
            c.count = count
            breached_passwords.append(c)

    logger.warning("=" * 50)
    if breached_passwords:
        print(
            "Found {} previously breached password{}:".format(
                len(breached_passwords), "s" if len(breached_passwords) > 1 else ""
            )
        )
        for c in breached_passwords:
            print(
                "{}:{}:{}".format(
                    c.display(), c.password if print_plaintext else c.sha1, c.count
                )
            )
    else:
        print("None of your passwords have been found breached.")
