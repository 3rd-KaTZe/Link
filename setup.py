# coding=utf-8
__author__ = 'etcher3rd'
import sys
from cx_Freeze import setup, Executable

from main import __version__

build_exe_options = {
    'packages': ['os', 'socket', 'sys', 'threading', 'json', 'select', 'time', 'datetime'],
    'include_files': [
        (r"config_Helo-Link.csv", r"config_Helo-Link.csv"),
        (r"z_Data_Dico.csv", r"z_Data_Dico.csv"),
    ],
}

setup(name='KaTZeLink',
      version=__version__.replace('alpha', '0.0.0.').replace('beta', '0.0.'),
      description="Katze Link",
      options={'build_exe': build_exe_options},
      executables=[
          Executable('helo_link.py',
                     base='Win32GUI',
                     icon='./ui/link.ico',
                     targetName='KatzeLink.exe'
          )],
      requires=['PyQt5', 'wmi'],
)