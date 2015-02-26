# coding=utf-8
__author__ = 'etcher3rd'
__version__ = "alpha15"
__guid__ = '34dbf25d-1efc-4d19-956f-6f276f4fb78d'

import sys
import ctypes
from os import _exit

if __name__ == "__main__":
    if hasattr(sys, 'frozen'):
        sys.stdout = open("stdout.log", "w")
        sys.stderr = open("stderr.log", "w")
        # workaround for Windows Vista
        # noinspection PyBroadException
        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(__guid__)
        except:
            pass
    # noinspection PyUnresolvedReferences
    import helo_link
    _exit(0)
