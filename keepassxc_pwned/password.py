import sys
import time
import hashlib
from typing import Optional

import requests

from .log import logger

default_headers = {"User-Agent": "keepassxc-pwned"}


def request_password_hash(hash_head: str) -> Optional[requests.Response]:
    """
    Requests the Repsonse object for the corresponding hash head (5 chars)
    """
    url = "https://api.pwnedpasswords.com/range/" + hash_head
    res = requests.get(url, headers=default_headers)
    if res.status_code >= 400:
        if res.status_code == 429:
            logger.warning("Hit rate limit, waiting for 10 seconds... ")
            time.sleep(10)
            return request_password_hash(hash_head)
        else:
            # TODO: Create/Raise an exception so that it can be caught in different situations
            logger.critical(
                "Error fetching {}\n{}: {}".format(url, res.status_code, res.text)
            )
            sys.exit(1)
    return res


# Adapted from: https://github.com/mikepound/pwned-search/blob/8efd8ffedd398756e26d52ef51206ba6d8e28f57/pwned.py#L12
def lookup_pwned(passwd: Optional[str] = None, pw_hash: Optional[str] = None) -> int:
    """Returns number of times password was seen in pwned database"""
    if passwd is None and pw_hash is None:
        raise ValueError("You must pass either 'passwd' or 'pw_hash'")
    if pw_hash is None:
        pw_hash = hashlib.sha1(passwd.encode("utf-8")).hexdigest().upper()
    head, tail = pw_hash[:5], pw_hash[5:]
    res = request_password_hash(head)
    hashes = (line.split(":") for line in res.text.splitlines())
    count = next((int(count) for t, count in hashes if t == tail), 0)
    return count
