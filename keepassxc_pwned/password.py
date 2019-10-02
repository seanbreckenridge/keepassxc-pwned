import sys
import time
import hashlib
import logging
from typing import Optional

import requests


def log_err(msg: str, logger: Optional[logging.Logger] = None):
    if logger:
        logger.critical(msg)
    else:
        print(msg, file=sys.stderr)


def request_password_hash(hash_head: str, logger: Optional[logging.Logger] = None):
    """Requests the Repsonse object for the corresponding hash head (5 chars)"""
    url = "https://api.pwnedpasswords.com/range/" + hash_head
    res = requests.get(
        url, headers={"User-Agent": "Unofficial-KeePassXC-Password-Checker"}
    )
    if res.status_code == 429:
        log_err("Hit rate limit, waiting for 10 seconds... ", logger)
        time.sleep(10)
        return request_password_hash(hash_head)
    elif res.status_code >= 400:
        log_err(
            "Error fetching {}\n{}: {}".format(url, res.status_code, res.text), logger
        )
    else:
        return res


# Source: https://github.com/mikepound/pwned-search/blob/8efd8ffedd398756e26d52ef51206ba6d8e28f57/pwned.py#L12
def lookup_pwned(pwd: str, logger: Optional[logging.Logger] = None):
    """Returns hash and number of times password was seen in pwned database"""
    sha1pwd = hashlib.sha1(pwd.encode("utf-8")).hexdigest().upper()
    head, tail = sha1pwd[:5], sha1pwd[5:]
    res = request_password_hash(head, logger)
    hashes = (line.split(":") for line in res.text.splitlines())
    count = next((int(count) for t, count in hashes if t == tail), 0)
    return sha1pwd, count
