# test the command line interface

from copy import deepcopy

from .common import *

import pexpect
import shutil

test_kdbx_db = os.path.join(db_files, "empty.kdbx")

key_file = os.path.join(db_files, "empty_keyfile")
key_protected_kdbx_db = os.path.join(db_files, "empty_keyfile.kdbx")

protected_keyfile = os.path.join(db_files, "empty_password_is_test.kdbx")

# no password
def test_kdbx_file():
    p = shlex.split("keepassxc_pwned {}".format(test_kdbx_db))
    child_proc = pexpect.spawn(" ".join(p), cwd=this_dir)
    child_proc.wait()
    output = child_proc.read().decode("utf-8")
    last_line = output.splitlines()[-1]
    assert len(output.splitlines()) == 1
    assert last_line == "None of your passwords have been found breached."


# no password, with key file
def test_key_file():
    p = shlex.split("keepassxc_pwned -k {} {}".format(key_file, key_protected_kdbx_db))
    child_proc = pexpect.spawn(" ".join(p), cwd=this_dir)
    child_proc.wait()
    output = child_proc.read().decode("utf-8")
    last_line = output.splitlines()[-1]
    assert len(output.splitlines()) == 1
    assert last_line == "None of your passwords have been found breached."


def test_environment_auth():
    keepassxc_binary_loc = shutil.which("keepassxc_pwned")
    p = shlex.split("{} {}".format(keepassxc_binary_loc, protected_keyfile))
    environment = deepcopy(os.environ)
    environment["KEEPASSXC_PWNED_PASSWD"] = "test"
    child_proc = pexpect.spawn(
        " ".join(p), cwd=this_dir, env=environment
    )
    child_proc.wait()
    output = child_proc.read().decode("utf-8")
    last_line = output.splitlines()[-1]
    assert len(output.splitlines()) == 1
    assert last_line == "None of your passwords have been found breached."

