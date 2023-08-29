# KeepassXC-Pwned

### Project Status

The functionality to check passwords again the HIBP database has been built into keepassxc since version 2.6.0 (Database > Database Reports > HIBP). This project should still work on keepassxc versions `<2.6.0`, though fails due to what I assume is a change in the specification for the `keepassxc-cli` export post version 2.6.0. I don't plan to update this to work with keepassxc 2.6.0 seeing as the functionality this offered is now built-in. This can still be used as a utility module to check passwords against the HIBP database:

In python code:

```
from keepassxc_pwned import check_password
check_password("password")
```

_Note: `check_password` doesn't attempt to do any rate limiting._

or, by entering the password manually:

```
$ python3 -m keepassxc_pwned
Password to check:
Found password 1054 times!
```
---- 

This checks a [KeePassXC](https://keepassxc.org/) database against previously cracked [haveibeenpwned](https://haveibeenpwned.com/) passwords.

#### Requirements

- `keepassxc-cli` binary (typically installed with KeePassXC)
- python 3.6 or above

#### Install

`pip3 install keepassxc-pwned`

#### Run

Run: `keepassxc_pwned ~/database.kdbx`

```
Usage: keepassxc_pwned [OPTIONS] DATABASE

  Check a keepassxc database against previously cracked haveibeenpwned
  passwords

Options:
  -p, --plaintext       Print breached passwords in plaintext; defaults to
                        sha1 hashes.

  -k, --key-file PATH   Key file for the database
  -v, --verbose         Print debug messages
  -q, --quiet           Don't print status messages, just the summary
  --keepassxc-cli PATH  Specify a different location for the keepassxc-cli
                        binary

  --help                Show this message and exit.
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
Found 1 previously breached password:
minecraft:5BAA61E4C9B93F3F0682250B6CF8331B7EE68FD8:3
```

#### Privacy concerns

This tool only transmits the first 5 characters of the SHA-1 hash of your passwords.
You can read more about that [here](https://www.troyhunt.com/ive-just-launched-pwned-passwords-version-2/#cloudflareprivacyandkanonymity).

#### Troubleshooting

If `keepassxc-cli` is named something else on your installation of KeepassXC, specify the full path by providing the `--keepassxc-cli` flag, like: `keepassxc_pwned --keepassxc-cli "$(which keepassxc.cli)" ~/Documents/updated_database.kdbx`

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

- Clone this repository
- Install dev dependencies: `pip3 install -r requirements-dev.txt`
- `mypy keepassxc_pwned`
- `pytest`
