import os
import shlex
import pathlib

import pytest

from keepassxc_pwned.parser import Database, Credential

this_dir = os.path.abspath(os.path.dirname(__file__))
db_files = os.path.join(this_dir, "database_files")
