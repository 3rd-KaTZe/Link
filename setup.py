# coding=utf-8
__author__ = 'etcher3rd'

import sys
from cx_Freeze import setup, Executable


from helo_link import __version__

build_exe_options = {
    'packages': ['os', 'socket', 'sys', 'threading', 'json', 'select', 'time', 'datetime'],
    }

base = None

if sys.platform == 'win32':
    base = 'Win32GUI'
    # base = 'console'

setup(  name = 'EAMI',
        version = __version__,
        description = "Etcher's Automated Mod Installer",
        options = {'build_exe': build_exe_options},
        executables = [
            Executable('helo_link.py',
                       base=base,
            )],
        )