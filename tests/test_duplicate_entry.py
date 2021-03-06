import vcr

from .common import *

from keepassxc_pwned.cli import main_wrapper
from keepassxc_pwned.parser import Database

db_file_loc = os.path.join(db_files, "duplicate_entry.kdbx")
db_pw = "duplicate_entry"


@pytest.fixture()
def database():
    db: Database = Database(pathlib.Path(db_file_loc))
    db._password = db_pw
    return db


def test_entry_count(database):
    assert len(database.credentials) == 3


# pass -q flag
@vcr.use_cassette("tests/vcr_cassettes/test_default.yaml")
def test_default(capsys, caplog):
    os.environ["KEEPASSXC_PWNED_PASSWD"] = "duplicate_entry"
    main_wrapper(False, None, False, True, db_file_loc, None)
    captured = capsys.readouterr()
    captured_lines = captured.out.splitlines()
    for output, expected in zip(
            captured_lines,
        [
            "Found 3 previously breached passwords:",
            "entry:5BAA61E4C9B93F3F0682250B6CF8331B7EE68FD8:3730471",
            "entry:5BAA61E4C9B93F3F0682250B6CF8331B7EE68FD8:3730471",
            "5BAA61E4C9B93F3F0682250B6CF8331B7EE68FD8:5BAA61E4C9B93F3F0682250B6CF8331B7EE68FD8:3730471",
        ],
    ):
        assert output == expected
    assert len(captured_lines) == 4
