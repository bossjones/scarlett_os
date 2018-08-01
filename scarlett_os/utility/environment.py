# -*- coding: utf-8 -*-

from __future__ import with_statement, division

import sys

# SOURCE: https://stackoverflow.com/questions/1871549/determine-if-python-is-running-inside-virtualenv
def is_venv():
    return (hasattr(sys, 'real_prefix') or
            (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))
