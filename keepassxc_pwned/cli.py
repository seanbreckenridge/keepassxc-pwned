from typing import Mapping, Tuple

import click

from .parser import Database, Credential
from .utils import PasswordCache
from .log import logger


@click.command()
@click.option(
    "-p",
    "--plaintext",
    default=False,
    is_flag=True,
    help="Print breached passwords in plaintext; defaults to sha1 hashes.",
)
@click.option("-k", "--key-file", required=False, type=click.Path(exists=True))
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
@click.argument("database", required=1, type=click.Path(exists=True))
def main(plaintext, key_file, verbose, quiet, database):
    # TODO: implement plaintext, verbose, quiet
    db: Database = Database(database, key_file)
    # maps sha1 hashes to credentials and their occurence counts
    breached_passwords: Mapping[str, Tuple[Credential, int]] = PasswordCache()
    for c in db.credentials:
        logger.info("Checking password for {}...".format(c.display()))
        count: int = breached_passwords[c.sha1]
        if count != 0:
            logger.info(
                "Found password for '{}' {} times in the dataset!".format(
                    c.display(), count
                )
            )
    logger.warning("=" * 50)
    if breached_passwords:
        print(
            "Found {} previously breached password{}:".format(
                len(breached_passwords), "s" if len(breached_passwords) > 1 else ""
            )
        )
        for c in breached_passwords:
            print("{}:{}:{}".format(c.display(), c.sha1, c.count))
    else:
        print("None of your passwords have been found breached.")
