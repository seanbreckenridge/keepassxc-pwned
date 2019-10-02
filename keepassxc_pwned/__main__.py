import sys
import getpass

from keepassxc_pwned import check_password

pw = getpass.getpass("Password to check: ")
count = check_password(pw)
if count > 0:
    print("Found password {} times!".format(count))
    sys.exit(1)
else:
    print("Could not find that password in the dataset.")
sys.exit(0)
