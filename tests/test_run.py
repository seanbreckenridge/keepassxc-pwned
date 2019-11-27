"""
Assumes keepassxc_pwned is already installed

Requires pexpect (pip3 install --user pexpect)
"""

import os
import shlex

import pexpect

this_dir = os.path.abspath(os.path.dirname(__file__))
test_kdbx_db = os.path.join(this_dir, 'password_is_test.kdbx')

def test_kdbx_file():
    p = shlex.split("keepassxc_pwned {}".format(test_kdbx_db))
    child_proc = pexpect.spawn(' '.join(p), cwd=this_dir)
    # wait for password prompt
    child_proc.expect("Insert password for*")
    child_proc.sendline("test")
    child_proc.wait()
    output = child_proc.read().decode('utf-8')
    assert "Checking password for site 2..." in output
    assert "Checking password for site one..." in output
    assert "Found password for 'site one'" in output
    assert "site one:5BAA61E4C9B93F3F0682250B6CF8331B7EE68FD8" in output

if __name__ == "__main__":
    test_kdbx_file()
