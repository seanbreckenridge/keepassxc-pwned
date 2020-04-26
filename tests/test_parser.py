# test Credential/Database functions

from unittest.mock import patch

from keepassxc_pwned.parser import Database, Credential

from .common import *

db_file_loc = os.path.join(db_files, "duplicate_entry.kdbx")


@pytest.fixture()
def database():
    db: Database = Database(pathlib.Path(db_file_loc))
    db._password = "duplicate_entry"
    return db


@pytest.fixture()
def empty_credential(database):
    credentials = database.credentials
    cred0 = credentials[0]
    for attr in Credential.parsed_attrs:
        if hasattr(cred0, attr):
            delattr(cred0, attr)
    return cred0


@pytest.fixture()
def basic_credential(database):
    credentials = database.credentials
    cred0 = credentials[0]
    return cred0


def test_matching_credentials(database):
    one, two, incomplete = database.credentials
    assert one == two
    assert one.password == two.password
    assert incomplete.password == two.password
    assert incomplete.username is None
    assert incomplete.title is None
    assert one._sha1 is None
    assert one.sha1 == "5BAA61E4C9B93F3F0682250B6CF8331B7EE68FD8"
    assert one._sha1 == "5BAA61E4C9B93F3F0682250B6CF8331B7EE68FD8"


def test_database_cached_values(database):
    assert database._xml_tree is None
    database.xml_tree
    assert database._xml_tree is not None
    database.xml_tree
    assert database._credentials is None
    database.credentials
    assert database._credentials is not None
    database.credentials


# @patch("getpass.getpass")
# def test_database_password(patched_getpass):
#    patched_getpass.return_value = ""
#    database: Database = Database(pathlib.Path(db_file_loc))
#    assert database._password is None
#    assert database._credentials is None
#    with pytest.raises(SystemExit):
#        database.credentials
#    assert database._credentials is None
#


def test_type_not_credential(basic_credential):
    assert "5" != basic_credential


def test_no_attributes(empty_credential, basic_credential):
    setattr(empty_credential, "password",
            "doesnt_match")  # causes attribute error else
    assert empty_credential == basic_credential


def test_display_fails(empty_credential):
    assert empty_credential.display() is None
