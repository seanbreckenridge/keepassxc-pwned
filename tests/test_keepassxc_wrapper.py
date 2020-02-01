from distutils.version import StrictVersion

from .common import *

from keepassxc_pwned.keepass_wrapper import KeepassWrapper

def test_is_strict_version():
    assert isinstance(KeepassWrapper.version(), StrictVersion)


