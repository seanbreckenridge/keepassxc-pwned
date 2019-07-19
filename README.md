# KeepassXC-Pwned

[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

This checks a KeePassXC database against previously cracked [haveibeenpwned](https://haveibeenpwned.com/) passwords.

#### Requirements

* `keepassxc-cli` binary, which is installed with `brew cask install keepassxc`.
* python 3.7

If you get the following error while using `keepassxc-cli`:

```
dyld: Library not loaded: /usr/local/opt/quazip/lib/libquazip.1.dylib
  Referenced from: /usr/local/bin/keepassxc-cli
  Reason: image not found
Abort trap: 6
```

... running `brew install quazip` should fix that.


Install: `pip3 install git+https://github.com/seanbreckenridge/keepassxc-pwned`

Run: `keepassxc_pwned ~/database.kdbx`

Pass the `--plaintext` flag to print breached passwords in plaintext, e.g. `keepassxc_pwned ~/database.kdbx --plaintext`

Sample Output:

```
Checking password for Apple... ✓
Checking password for Discord... ✓
Checking password for Dropbox... ✓
Checking password for Github... ✓
Checking password for Heroku... ✓
Checking password for Mega... ✓
Checking password for Spotify... ✓
Checking password for Steam... ✓
Checking password for Streamable... ✓
Checking password for Vimeo... ✓
Checking password for Venmo... ✓
Checking password for minecraft...
Found password for 'minecraft' 5 times in the dataset!
Checking password for stackoverflow... ✓
==================================================
Found 1 previously breached password:
minecraft:E38AD214943DAAD1D64C102FAEC29DE4AFE9DA3D:5
```
