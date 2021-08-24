import sys
import vcr

from unittest.mock import patch
from .common import *

from getpass import getpass


@vcr.use_cassette("tests/vcr_cassettes/test_user_password_fails.yaml")
@patch("getpass.getpass")
def test_user_input_password_found(getpass, capsys):
    getpass.return_value = "test"
    with pytest.raises(SystemExit):
        import keepassxc_pwned.__main__
    captured = capsys.readouterr()
    captured_lines = captured.out.splitlines()
    assert len(captured_lines) == 1
    assert captured_lines[0] == "Found password 76479 times!"


@vcr.use_cassette("tests/vcr_cassettes/test_user_password_succeeds.yaml")
@patch("getpass.getpass")
def test_user_input_password_not_found(getpass, capsys):
    getpass.return_value = "^lL2fY@B82C[UHbpd`B[0QO#Ky5Im-D+63F%nwe40iQ*Pt`Sqyn6Q0u254.2I?Vf4!+U83[lYl[=E6iU6v=hZ-9a5y3=o.^VO36="
    import keepassxc_pwned.__main__

    captured = capsys.readouterr()
    captured_lines = captured.out.splitlines()
    assert len(captured_lines) == 1
    assert captured_lines[0] == "Could not find that password in the dataset."
    del sys.modules['keepassxc_pwned.__main__']
