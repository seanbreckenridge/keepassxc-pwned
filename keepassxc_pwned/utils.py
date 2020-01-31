from time import sleep
from collections import defaultdict

from .password import lookup_pwned


class AutoRepr:
    """
    Automatically creates a repr for a class given a list of attributes
    """

    # must have self.__class__.attrs set
    def __repr__(self) -> str:
        assert self.__class__.attrs is not None

        return "{}({})".format(
            self.__class__.__name__,
            ", ".join(
                [
                    "{}={}".format(a, repr(getattr(self, a, None)))
                    for a in self.__class__.attrs
                ]
            ),
        )

    def __str__(self) -> str:
        return self.__repr__()


class PasswordCache(defaultdict):
    """
    If the password hash has not been requested before, requests it.
    If you have the same password for many entries, this would only request that once.
    """

    def __missing__(self, key) -> int:
        count: int = lookup_pwned(pw_hash=key)
        sleep(2)
        return count
