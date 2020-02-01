import time
import hashlib

from typing import Optional

import requests

from .log import logger
from .exceptions import PwnedPasswordException


default_headers = {"User-Agent": "keepassxc-pwned"}


def request_password_hash(hash_head: str) -> requests.Response:
    """
    Requests the Response object for the corresponding hash head (5 chars)
    Raises PwnedPasswordException on unrecoverable errors
    """
    url = "https://api.pwnedpasswords.com/range/" + hash_head
    logger.debug("Requesting {}".format(url))
    res = requests.get(url, headers=default_headers)
    if res.status_code >= 400:
        # on occasion I've had random 409 cloudflare errors
        if res.status_code in [400, 403, 404]: # https://haveibeenpwned.com/API/v2#ResponseCodes
            raise PwnedPasswordException(
                {"url": url, "status_code": res.status_code, "http_text": res.text}
            )
        else:
            logger.warning("Request failed, retrying...")
            time.sleep(10)
            return request_password_hash(hash_head)
    return res


# Adapted from: https://github.com/mikepound/pwned-search/blob/8efd8ffedd398756e26d52ef51206ba6d8e28f57/pwned.py#L12
def lookup_pwned(passwd: Optional[str] = None, pw_hash: Optional[str] = None) -> int:
    """
    Returns number of times password was seen in pwned database
    Raises PwnedPasswordException on unrecoverable errors
    """
    if pw_hash is None:
        if passwd is not None:
            pw_hash = hashlib.sha1(passwd.encode("utf-8")).hexdigest().upper()
        else:
            raise ValueError("You must pass either 'passwd' or 'pw_hash'")
    head, tail = pw_hash[:5], pw_hash[5:]
    res: requests.Response = request_password_hash(head)
    hashes = (line.split(":") for line in res.text.splitlines())
    count = next((int(count) for t, count in hashes if t == tail), 0)
    return count
