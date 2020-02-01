from typing import Mapping, Any

from .utils import AutoRepr


class PwnedPasswordException(AutoRepr, Exception):
    """
    PwnedPassword API Client Errors (>=400, excluding 429)
    """

    attrs = ["url", "status_code", "http_text"]

    def __init__(self, message: Mapping[str, Any]):
        self.url = message["url"]
        self.status_code = message["status_code"]
        self.http_text = message["http_text"]

        super(PwnedPasswordException, self).__init__(str(self))

    def __str__(self) -> str:
        return "Error fetching {}\n{}: {}".format(
            self.url, self.status_code, self.http_text
        )
