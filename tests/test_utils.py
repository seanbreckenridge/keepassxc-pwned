# test AutoRepr

import logging

from keepassxc_pwned.utils import AutoRepr
from keepassxc_pwned.log import logger, setup_logs

from .common import *


class Entry(AutoRepr):

    attrs = ["one", "two"]

    def __init__(self, one, two):
        self.one = one
        self.two = two


@pytest.fixture()
def entry():
    e = Entry(1, 2)
    return e


def test_repr(entry):
    repr_entry = repr(entry)
    assert isinstance(repr_entry, str)
    assert repr_entry == "Entry(one=1, two=2)"


def test_str(entry):
    str_entry = str(entry)
    assert isinstance(str_entry, str)
    assert str_entry == "Entry(one=1, two=2)"


def test_logs(caplog):
    # call setup_logs again to make sure it exits early
    with caplog.at_level(logging.INFO, logger="keepassxc_pwned"):
        logger.info("message one")
    setup_logs()
    setup_logs()
    with caplog.at_level(logging.INFO, logger="keepassxc_pwned"):
        logger.info("message two")
    assert len(caplog.records) == 2
    assert "message one" == caplog.records[0].getMessage()
    assert "message two" == caplog.records[1].getMessage()
