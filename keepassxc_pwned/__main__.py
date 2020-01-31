import sys

from getpass import getpass

from . import check_password

count: int = check_password(getpass("Password to check: "))
if count > 0:
    print("Found password {} times!".format(count))
    sys.exit(1)
else:
    print("Could not find that password in the dataset.")
