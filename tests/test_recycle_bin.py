# Make sure that entries in the recycle bin are ignored

from .common import *


@pytest.fixture
def database():
    db_file_loc = os.path.join(db_files, "recycle_bin_test.kdbx")
    db = Database(pathlib.Path(db_file_loc))
    db._password = "recycle_bin_test"
    return db


def test_count(database):
    """
    There are 3 items in the test_recycle_bin.kdbx that exist
    but one is in the Recycle Bin, make sure that its ignored
    """
    assert len(database.credentials) == 2


def test_credentials(database):
    credentials = database.credentials
    assert type(credentials[0]) == Credential
    cred = credentials[0]
    assert cred.sha1 == "30274C47903BD1BAC7633BBF09743149EBAB805F"
    assert cred.password == "passwd"
    assert credentials[0] != credentials[1]
