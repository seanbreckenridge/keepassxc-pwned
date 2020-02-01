from .log import setup_logs

# called when anything is imported from this package
setup_logs()

from .password import lookup_pwned as check_password
from .exceptions import PwnedPasswordException
