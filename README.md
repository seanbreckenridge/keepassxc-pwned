# KeepassXC-Pwned

[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

This checks a [KeePassXC](https://keepassxc.org/) database against previously cracked [haveibeenpwned](https://haveibeenpwned.com/) passwords.

#### Requirements

* `keepassxc-cli` binary (typically installed with KeePassXC)
* python 3.7 or above

#### Install

`pip3 install keepassxc-pwned`

#### Run

Run: `keepassxc_pwned ~/database.kdbx`

```
Check a keepassxc database against previously cracked haveibeenpwned passwords

Usage:
    keepassxc_pwned [--help]
    keepassxc_pwned [-pq] [-k KEY] <KDBX_DATABASE_FILE>

KDBX_DATABASE_FILE            The path to your
                              keepassxc database file
-p, --plaintext               Print breached passwords in plaintext;
                              defaults to sha1 hashes
-q, --no-logs                 Don't print status messages,
                              just the summary message
-k KEY, --key-file=KEY_FILE   Key file for the database

Examples:
    keepassxc_pwned ~/database.kdbx
    keepassxc_pwned ~/database.kdbx --plaintext
    keepassxc_pwned -k ~/key_file ~/database.kdbx
```

Sample Run:

```
$ keepassxc_pwned ~/Documents/updated_database.kdbx
Insert password for /home/sean/Documents/updated_database.kdbx:
Checking password for Amazon...
Checking password for Github...
Checking password for Netflix...
Checking password for Steam...
Checking password for letterboxd...
Checking password for linkedin...
Checking password for minecraft...
Found password for 'minecraft' 3 times in the dataset!
Checking password for soundcloud...
Checking password for stackoverflow...
Checking password for wikipedia...
==================================================
Found 1 previously breached password:
minecraft:5BAA61E4C9B93F3F0682250B6CF8331B7EE68FD8:3
```

You can also import this to use in python code...

```
from keepassxc_pwned import check_password
check_password("password")
```

*Note: `check_password` doesn't attempt to do any rate limiting.*

... or enter the password manually...

```
$ python3 -m keepassxc_pwned
Password to check:
Found password 1054 times!
```

#### Troubleshooting

If you get the following error while using `keepassxc-cli`:

```
dyld: Library not loaded: /usr/local/opt/quazip/lib/libquazip.1.dylib
  Referenced from: /usr/local/bin/keepassxc-cli
  Reason: image not found
Abort trap: 6
```

... installing `quazip` should fix that:

- `brew install quazip` (Mac)

- `sudo apt install libquazip-dev` (Linux)

If `keepassxc-cli` fails with an error message like "Invalid Command extract.", the command was changed in KeePassXC 2.5.0, and is now called `export`. Upgrade KeePassXC to the latest version, and try again.

#### Tests

* Clone this repository
* Install `pexpect` and `pytest`: `pip3 install pexpect pytest`
* Run `pytest` in the root directory

