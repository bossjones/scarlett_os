#!/usr/bin/env python3
"""Print the content of an environment variable on stdout."""
import os
import sys

# SOURCE: https://github.com/GNOME/pitivi/blob/b8b22123966cff0ba513300ef2b4fd3dec624c5a/getenvvar.py

print(os.environ.get(sys.argv[1], ''))
