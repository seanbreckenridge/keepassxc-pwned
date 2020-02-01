# Test non-interactive authentication methods

from .common import *

test_kdbx_db = os.path.join(db_files, "empty.kdbx")

key_file = os.path.join(db_files, "empty_keyfile")
key_protected_kdbx_db = os.path.join(db_files, "empty_keyfile.kdbx")

kdbx_password = "password"


@pytest.fixture()
def empty_db():
    db = Database(pathlib.Path(test_kdbx_db))
    db._password = kdbx_password
    return db


@pytest.fixture()
def empty_db_keyfile():
    db = Database(pathlib.Path(key_protected_kdbx_db), pathlib.Path(key_file))
    db._password = kdbx_password
    return db


@pytest.fixture()
def empty_db_with_environment_var():
    os.environ["KEEPASSXC_PWNED_PASSWD"] = kdbx_password
    db = Database(pathlib.Path(test_kdbx_db))
    return db


def test_empty_db(empty_db):
    assert len(empty_db.credentials) == 0


def test_empty_db_keyfile(empty_db_keyfile):
    assert len(empty_db_keyfile.credentials) == 0


def test_empty_db_with_environment_var(empty_db_with_environment_var):
    assert len(empty_db_with_environment_var.credentials) == 0

