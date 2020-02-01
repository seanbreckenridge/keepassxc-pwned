import pathlib
import logging

from typing import Mapping, List

import click

from .log import logger, set_level
from .exceptions import PwnedPasswordException


@click.command()
@click.option(
    "-p",
    "--plaintext",
    default=False,
    is_flag=True,
    help="Print breached passwords in plaintext; defaults to sha1 hashes.",
)
@click.option(
    "-k",
    "--key-file",
    required=False,
    type=click.Path(exists=True),
    help="Key file for the database",
)
@click.option(
    "-v", "--verbose", default=False, is_flag=True, help="Print debug messages"
)
@click.option(
    "-q",
    "--quiet",
    default=False,
    is_flag=True,
    help="Don't print status messages, just the summary",
)
@click.argument("database", required=True, type=click.Path(exists=True))
def main(plaintext, key_file, verbose, quiet, database):
    """Check a keepassxc database against previously cracked haveibeenpwned passwords"""
    main_wrapper(plaintext, key_file, verbose, quiet, database)


def main_wrapper(plaintext, key_file, verbose, quiet, database):
    """Called from main click command"""

    # setup logs before other imports to ensure correct log level
    log_level: int = logging.INFO
    # cant run verbose and quiet simultaneously, choose higher value
    if verbose:
        log_level = logging.DEBUG
    elif quiet:
        log_level = logging.ERROR

    set_level(log_level)

    from .parser import Database, Credential
    from .cache import PasswordCache

    if key_file is not None:
        key_file: pathlib.Path = pathlib.Path(key_file)
    db: Database = Database(pathlib.Path(database), key_file)
    # maps sha1 hashes to credentials and their occurrence counts
    breached_passwords: List[Credential] = []
    pw_cache: Mapping[str, int] = PasswordCache()
    for credential in db.credentials:
        logger.info("Checking password for {}...".format(credential.display()))
        # pw_cache __missing__ makes the http request to get the count
        try:
            occurrence_count = pw_cache[credential.sha1]
            if occurrence_count > 0:
                logger.info(
                    "Found password for '{}' {} times in the dataset!".format(
                        credential.display(), occurrence_count
                    )
                )
                breached_passwords.append(credential)
        except PwnedPasswordException as http_err:
            logger.critical(str(http_err))
            logger.critical("Ignoring previous entry due to HTTP error")
    breached_passwords_count = len(breached_passwords)
    if breached_passwords_count > 0:
        print(
            "Found {} previously breached password{}:".format(
                breached_passwords_count, "s" if breached_passwords_count > 1 else ""
            )
        )
        for credential in breached_passwords:
            display_pw: str = credential.password if plaintext else credential.sha1
            print(
                "{}:{}:{}".format(
                    credential.display(), display_pw, pw_cache[credential.sha1]
                )
            )
    else:
        print("None of your passwords have been found breached.")
