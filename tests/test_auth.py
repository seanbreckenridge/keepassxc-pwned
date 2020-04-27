# Test non-interactive authentication methods

from keepassxc_pwned.parser import Database
from keepassxc_pwned.cli import main_wrapper

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


def test_empty_db_raises_exit(empty_db):
    empty_db._password = "wrong password"
    with pytest.raises(SystemExit):
        empty_db._call_keepassxc_cli()
    assert empty_db._xml_tree is None


def test_empty_db_keyfile(empty_db_keyfile):
    assert len(empty_db_keyfile.credentials) == 0


def test_empty_db_with_environment_var(empty_db_with_environment_var):
    assert len(empty_db_with_environment_var.credentials) == 0


def test_keyfile_with_main_wrapper(capsys):
    os.environ["KEEPASSXC_PWNED_PASSWD"] = kdbx_password
    main_wrapper(False, key_file, False, True, key_protected_kdbx_db, None)
    captured = capsys.readouterr()
    captured_lines = captured.out.splitlines()
    assert 1 == len(captured_lines)
    assert captured_lines[
        0] == "None of your passwords have been found breached."
