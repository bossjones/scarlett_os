# -*- coding: utf-8 -*-

def check_python3_installed():
    import sys
    if sys.version_info < (3, 4) <= sys.version_info < (3, 5):
        print('ScarlettOS requires at least Python 3.4 or 3.3 to run.')
        sys.exit(1)


def get_current_os():
    import platform
    return platform.platform().split('-')
