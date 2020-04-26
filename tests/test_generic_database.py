"""
test edge cases for keepass databases
when there is no title/username for a entry
when theres no password
"""

import vcr
from unittest.mock import patch

from keepassxc_pwned.parser import Credential, Database
from keepassxc_pwned.cli import main_wrapper

from .common import *

db_file_loc = os.path.join(db_files, "generic_has_passwords.kdbx")


# no flags
@vcr.use_cassette("tests/vcr_cassettes/test_generic.yaml")
def test_default(capsys, caplog):
    os.environ["KEEPASSXC_PWNED_PASSWD"] = "generic_has_passwords"
    main_wrapper(False, None, False, False, db_file_loc)
    captured = capsys.readouterr()
    captured_lines = captured.out.splitlines()
    assert len(captured_lines) == 2
    assert captured_lines[0] == "Found 1 previously breached password:"
    assert (captured_lines[1] ==
            "breached_entry:74B0B92F4476AC6722C2232EB91CB79BC531311C:1054")
    captured_logs = list(map(lambda x: x.getMessage(), caplog.records))
    assert len(captured_logs) == 4
    assert captured_logs[0] == "Checking password for breached_entry..."
    assert (captured_logs[1] ==
            "Found password for 'breached_entry' 1054 times in the dataset!")
    assert captured_logs[2] == "Checking password for unbreached password..."
    assert (captured_logs[3] ==
            "Checking password for 3DFE1FD27BDF9870F23C3A5916D9A1495E492518..."
            )  # uses sha1 value since no title


# quiet flag
@vcr.use_cassette("tests/vcr_cassettes/test_quiet.yaml")
def test_quiet(capsys, caplog):
    os.environ["KEEPASSXC_PWNED_PASSWD"] = "generic_has_passwords"
    main_wrapper(False, None, False, True, db_file_loc)
    captured = capsys.readouterr()
    captured_lines = captured.out.splitlines()
    assert captured_lines[0] == "Found 1 previously breached password:"
    assert (captured_lines[1] ==
            "breached_entry:74B0B92F4476AC6722C2232EB91CB79BC531311C:1054")
    captured_logs = list(map(lambda x: x.getMessage(), caplog.records))
    assert len(captured_logs) == 0


# verbose flag
@vcr.use_cassette("tests/vcr_cassettes/test_verbose.yaml")
def test_verbose(capsys, caplog):
    os.environ["KEEPASSXC_PWNED_PASSWD"] = "generic_has_passwords"
    main_wrapper(False, None, True, False, db_file_loc)
    captured = capsys.readouterr()
    captured_lines = captured.out.splitlines()
    assert len(captured_lines) == 2
    assert captured_lines[0] == "Found 1 previously breached password:"
    assert (captured_lines[1] ==
            "breached_entry:74B0B92F4476AC6722C2232EB91CB79BC531311C:1054")
    captured_logs = list(map(lambda x: x.getMessage(), caplog.records))
    assert len(captured_logs) == 12
    assert (captured_logs[0] ==
            "Using password from KEEPASSXC_PWNED_PASSWD environment variable")
    assert captured_logs[1].startswith("keepassxc-cli version: ")
    assert captured_logs[2].startswith(
        "Export database command: keepassxc-cli")
    assert captured_logs[3].startswith(
        "Ignoring entry with no password: Credential(title='entry with no password'"
    )
    assert captured_logs[4] == "KeepassXC parsed entry count: 3"
    assert captured_logs[5] == "Checking password for breached_entry..."
    assert captured_logs[
        6] == "Requesting https://api.pwnedpasswords.com/range/74B0B"
    assert (captured_logs[7] ==
            "Found password for 'breached_entry' 1054 times in the dataset!")
    assert captured_logs[8] == "Checking password for unbreached password..."
    assert captured_logs[
        9] == "Requesting https://api.pwnedpasswords.com/range/92F9D"
    assert (
        captured_logs[10] ==
        "Checking password for 3DFE1FD27BDF9870F23C3A5916D9A1495E492518...")
    assert captured_logs[
        11] == "Requesting https://api.pwnedpasswords.com/range/3DFE1"


# plaintext with quiet
@vcr.use_cassette("tests/vcr_cassettes/test_plaintext.yaml")
def test_plaintext(capsys, caplog):
    main_wrapper(True, None, False, True, db_file_loc)
    captured = capsys.readouterr()
    captured_lines = captured.out.splitlines()
    # assert len(captured_lines) == 2
    assert captured_lines[0] == "Found 1 previously breached password:"
    assert captured_lines[-1] == "breached_entry:hunter42:1054"
