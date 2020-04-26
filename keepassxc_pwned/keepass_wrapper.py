import sys
import os
import shlex
import subprocess
import pathlib
import shutil

from typing import Optional, List
from functools import partial
from distutils.version import StrictVersion

from .log import logger

# redirect STDIN/STDERR from subprocess
subprocess_piped = partial(subprocess.run,
                           encoding="utf-8",
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)


class KeepassWrapper:
    """
    Functions that create a subprocess and call the keepassxc-cli shell command
    """

    KEEPASSXC_CLI_NAME = "keepassxc-cli"

    def __init__(self, keepassxc_cli_location: Optional[pathlib.Path] = None):
        """
        Create an instance of KeepassWrapper, with an optional
        path to the keepassxc-cli binary.


        Allow the path of the keepassxc-cli to be changed because
        some package managers (e.g. mint with snap) call
        this the binary keepassxc.cli
        """

        if keepassxc_cli_location is None:
            # search for keepassxc-cli which default name on $PATH
            keepassxc_cli_location = shutil.which(
                self.__class__.KEEPASSXC_CLI_NAME)
            if keepassxc_cli_location is None:
                logger.critical(
                    "Could not find a binary called {} on your $PATH.".format(
                        self.__class__.KEEPASSXC_CLI_NAME))
                sys.exit(1)
            self.keepassxc_cli_location: pathlib.Path = pathlib.Path(
                keepassxc_cli_location)
        else:
            self.keepassxc_cli_location = keepassxc_cli_location
        logger.debug("keepassxc-cli location: {}".format(
            self.keepassxc_cli_location))

    def version(self) -> StrictVersion:
        """Returns the KeepassXC Version"""
        version_proc: subprocess.CompletedProcess = subprocess_piped(
            [self.keepassxc_cli_location, "--version"])
        version_str: str = version_proc.stdout.strip()
        logger.debug("keepassxc cli version: {}".format(version_str))
        return StrictVersion(version_str)

    def backwards_compatible_export(self) -> str:
        """
        In KeepassXC version 2.5.0, the extract command was re-named to export
        Attempt to parse the version number and generate the correct subcommand
        """
        try:
            version: StrictVersion = self.version()
            if version < StrictVersion("2.5.0"):
                return "extract"
            else:
                return "export"
        except ValueError:
            return "export"

    def export_database(
        self,
        database_file: pathlib.Path,
        database_password: str,
        database_keyfile: Optional[pathlib.Path] = None,
        keepassxc_cli_location: Optional[pathlib.Path] = None,
    ) -> str:
        """Calls the keepassxc-cli export command, returns the output from the command"""

        command_parts: List[str] = [
            str(self.keepassxc_cli_location),
            self.backwards_compatible_export()
        ]
        if database_keyfile is not None:
            command_parts.extend(["-k", str(database_keyfile)])
        command_parts.append(str(database_file))
        command_str: str = " ".join(command_parts)
        logger.debug("Export database command: {}".format(command_str))
        keepassxc_output: subprocess.CompletedProcess = subprocess_piped(
            shlex.split(command_str),
            input=database_password,
        )
        if keepassxc_output.returncode != 0:
            logger.critical("Error communicating with {}".format(
                self.keepassxc_cli_location))
            logger.critical(keepassxc_output.stderr)
            sys.exit(1)
        # python doesn't like the version tag, remove the first line
        return keepassxc_output.stdout.split(os.linesep, 2)[-1]
