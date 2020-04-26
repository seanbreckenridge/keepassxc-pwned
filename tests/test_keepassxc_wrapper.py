from distutils.version import StrictVersion
from unittest.mock import patch

from keepassxc_pwned.keepass_wrapper import KeepassWrapper

from .common import *


class OldKeepassWrapper(KeepassWrapper):
    def version(self) -> StrictVersion:
        return StrictVersion("2.4.9")


class VersionError(KeepassWrapper):
    def version(self):
        return StrictVersion("2.5.a")  # raises ValueError


def test_is_strict_version():
    assert isinstance(KeepassWrapper().version(), StrictVersion)


def test_subcommand_old():
    assert OldKeepassWrapper().backwards_compatible_export() == "extract"


def test_subcommand_new():
    assert KeepassWrapper().backwards_compatible_export() == "export"


def test_issue_parsing_version_string():
    # should return "export" by default (newer syntax)
    assert VersionError().backwards_compatible_export() == "export"


@patch("shutil.which", return_value=None)
def test_no_keepass_cli(mock_shutil_which, caplog):
    # with default keepassxc-cli as --keepassxc-cli flag (binary)
    with pytest.raises(SystemExit):
        assert KeepassWrapper().verify_binary_exists()
    assert ("Could not find a binary called keepassxc-cli on your $PATH."
            in caplog.text)
