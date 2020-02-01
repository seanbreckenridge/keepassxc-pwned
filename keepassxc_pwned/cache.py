from time import sleep

from .password import lookup_pwned


class PasswordCache(dict):
    """
    If the password hash has not been requested before, requests it.
    If you have the same password for many entries, this would only request that once.
    """

    def __missing__(self, key: str) -> int:
        """
        Looks up the occurrence count for the sha1 value passed as key
        """
        count: int = lookup_pwned(pw_hash=key)
        sleep(2)
        self[key] = count
        return count

    def __setitem__(self, key: str, value: int):
        """
        sets sha1 -> occurence_count
        """
        super(PasswordCache, self).__setitem__(key, value)
