#!/usr/bin/env python3

"""Check a keepassxc database against previously cracked haveibeenpwned passwords

Usage:
    keepassxc_pwned <KDBX_DATABASE_FILE> [--plaintext]

Options:
    KDBX_DATABASE_FILE      The path to your keepassxc database file
    --plaintext             Print breached passwords in plaintext; defaults to sha1 hashes

Examples:
    keepassxc_pwned ~/database.kdbx
    keepassxc_pwned ~/database.kdbx --plaintext
"""

from keepassxc_pwned import *

# namedtuple representing an entry in the KeePassXC database and related information
fields = ['username', 'password', 'title', 'sha1', 'count']
Credential = namedtuple("Credential", fields, defaults=(None,) * len(fields))


def get_args():
    """Get the location of the KeePassXC database file as the first positional argument from command line"""
    args = docopt.docopt(__doc__)
    kdbx_db_location = args["<KDBX_DATABASE_FILE>"]
    if not os.path.exists(kdbx_db_location):
        print("Could not find a file at {}".format(kdbx_db_location))
        sys.exit(1)
    return kdbx_db_location, args["--plaintext"]


def subprocess_verify_binary():
    """Make sure the keepassxc-cli binary exists"""
    shell_output = subprocess.run(["which", "keepassxc-cli"], capture_output=True)
    if shell_output.returncode != 0:
        print("Could not find the keepassxc-cli binary. Make sure its on your PATH, or reinstall keepassxc with brew, like:\nbrew cask install keepassxc", file=sys.stderr)
        sys.exit(1)
    keepassxc_binary_location = shell_output.stdout.decode("utf-8").strip()
    return keepassxc_binary_location


def subprocess_process_xml(binary, kdbx_location):
    """Call the keepassxc-cli binary and extract the title, usernames and passwords"""

    credentials = []

    # use command line binary to passwords from kdbx in XML
    command = "{} extract {}".format(binary, kdbx_location)
    password = getpass.getpass("Insert password for {}: ".format(kdbx_location))
    keepassxc_output = subprocess.run(shlex.split(command), input=password,
                                      encoding='utf-8', stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)
    if keepassxc_output.returncode != 0:
        print(keepassxc_output.stderr, file=sys.stderr)
        sys.exit(1)

    # python doesnt like the version tag, remove the first line
    keepass_xml_str = keepassxc_output.stdout.split(os.linesep, 2)[-1]
    password_xml_tree = ET.fromstring(text=keepass_xml_str)
    for group in password_xml_tree.find("Root").iter("Group"):

        # ignore deleted passwords
        if group.find("Name").text == "Recycle Bin":
            continue

        # grab username, title, and passwords
        for entry in group.iter("Entry"):
            c = Credential()
            for str_node in entry.iter("String"):
                key = str_node.find("Key").text
                value = str_node.find("Value").text

                if key == "Title": c = c._replace(title=value)
                elif key == "UserName": c = c._replace(username=value)
                elif key == "Password": c = c._replace(password=value)

            if c.password is not None and c not in credentials:
                credentials.append(c)

    return credentials


def safe_api_get(hash_head):
    """Requests the Repsonse object for the corresponding hash head (5 chars)"""
    url = 'https://api.pwnedpasswords.com/range/' + hash_head
    res = requests.get(url, headers={"User-Agent": "Unofficial-KeePassXC-Password-Checker"})
    if res.status_code == 429:
        print("Hit rate limit, sleeping for 10 seconds... ", file=sys.stderr)
        time.sleep(10)
        return safe_api_get(hash_head)
    elif res.status_code != 200:
        raise RuntimeError("Error fetching {}\n{}: {}".format(url, res.status_code, res.text))
    else:
        time.sleep(1.5)
        return res


# Source: https://github.com/mikepound/pwned-search/blob/8efd8ffedd398756e26d52ef51206ba6d8e28f57/pwned.py#L12
def lookup_pwned_api(pwd):
    """Returns hash and number of times password was seen in pwned database"""
    sha1pwd = hashlib.sha1(pwd.encode('utf-8')).hexdigest().upper()
    head, tail = sha1pwd[:5], sha1pwd[5:]
    res = safe_api_get(head)
    hashes = (line.split(':') for line in res.text.splitlines())
    count = next((int(count) for t, count in hashes if t == tail), 0)
    return sha1pwd, count


def main():
    kdbx_db_location, print_plaintext = get_args()
    keepassxc_binary_location = subprocess_verify_binary()
    credentials = subprocess_process_xml(keepassxc_binary_location, kdbx_db_location)
    breached_passwords = []
    for c in credentials:
        title = c.title if c.title is not None else c.username
        print("Checking password for {}...".format(title), end="")
        sys.stdout.flush()
        sha1, count = lookup_pwned_api(c.password)
        if count != 0:
            print("\nFound password for '{}' {} times in the dataset!".format(title, count))
            c = c._replace(sha1=sha1)
            c = c._replace(count=count)
            breached_passwords.append(c)
        else:
            print(" ✓")
        time.sleep(1.5)

    print("=" * 50)
    if breached_passwords:
        print("Found {} previously breached password{}:".format(
                len(breached_passwords),
                "s" if len(breached_passwords) > 1 else ""
             ))
        for c in breached_passwords:
            title = c.title if c.title is not None else c.username
            print("{}:{}:{}".format(title, c.password if print_plaintext else c.sha1, c.count))
    else:
        print("None of your passwords were found in the dataset 👍")
