import logging
import pathlib
import hashlib
import xml.etree.cElementTree as ET

from getpass import getpass
from typing import List, Optional

from .log import logger
from .utils import AutoRepr
from .keepass_wrapper import KeepassWrapper


class Credential(AutoRepr):

    # ordering for repr
    attrs = ["title", "username", "password", "sha1"]

    # ordering for display
    display_attrs = ["title", "username", "sha1"]

    # attributes to extract from XML
    parsed_attrs = {"title", "username", "password"}

    def __init__(self, xml_entry: ET.Element):
        self._xml_entry = xml_entry
        for str_node in filter(lambda e: e.tag == "String", list(xml_entry)):
            key: str = str_node.find("Key").text.lower()
            value: str = str_node.find("Value").text

            if key in self.__class__.parsed_attrs:
                if value is not None:
                    setattr(self, key, value)

        if not hasattr(self, "password"):
            raise ValueError("Ignoring entry with no password: {}".format(self))

        self._sha1: Optional[str] = None

    def _warn_missing_attr(self, attr: str):
        """If the debug flag is set, warns the user if there is a missing attribute"""
        if not hasattr(self, attr):
            logger.warning("Missing {} on {}".format(attr, self))

    @property
    def sha1(self):
        if self._sha1 is None:
            if self.password is not None:
                self._sha1 = (
                    hashlib.sha1(self.password.encode("utf-8")).hexdigest().upper()
                )
        return self._sha1

    def __hash__(self) -> int:
        return hash(self.sha1)

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
        # must have at least a password, which would be displayed as sha1
        for a in self.__class__.display_attrs:
            try:
                return getattr(self, a)
            except AttributeError:
                pass


class Database(AutoRepr):

    attrs = ["database_file", "key_file", "logger"]

    def __init__(
        self,
        database_file: pathlib.Path,
        key_file: Optional[pathlib.Path] = None,
        logger: Optional[logging.Logger] = logger,
    ):
        self.database_file = database_file
        self.key_file = key_file
        self.logger = logger

        self._xml_tree: Optional[ET] = None
        self._password: Optional[str] = None
        self._credentials: Optional[List[Credential]] = None

    @property
    def password(self) -> str:
        if self._password is not None:
            return self._password
        else:
            self._password = getpass(
                "Insert password for {}: ".format(self.database_file)
            )
            return self._password

    @property
    def xml_tree(self) -> ET:
        self._call_keepassxc_cli()
        return self._xml_tree

    def _call_keepassxc_cli(self) -> None:
        """
        Calls the keepassxc-cli export as a subprocess
        Sets the '_xml_tree' attribute to the XML representation of the database
        """
        if self._xml_tree is not None:
            return  # already called, use cached value
        keepass_export_process_output: str = KeepassWrapper.export_database(
            database_file=self.database_file,
            database_password=self.password,
            database_keyfile=self.key_file,
        )
        self._xml_tree = ET.fromstring(keepass_export_process_output)

    @property
    def credentials(self) -> List[Credential]:
        if self._credentials is not None:
            return self._credentials
        self._credentials = []
        for group in self.xml_tree.find("Root").iter("Group"):
            # ignore deleted passwords
            if group.find("Name").text == "Recycle Bin":
                continue
            # grab username, title, and passwords
            for entry in filter(lambda g: g.tag == "Entry", list(group)):
                try:
                    cred = Credential(entry)
                    self._credentials.append(cred)
                except ValueError as no_pw:
                    logger.debug(str(no_pw))
        return self._credentials
