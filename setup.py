# coding=utf-8
__author__ = 'etcher3rd'

import sys

from cx_Freeze import setup, Executable
# from distutils.core import setup
# from esky import bdist_esky


from helo_link import __version__


"""
import os
import socket, select, sys, threading
import time, datetime
import json

from queue import Queue

import ws_protocol_00
import ws_handshake_00
import sbr_string
import sbr_data
import logging
"""

build_exe_options = {
    'packages': ['os', 'socket', 'sys', 'threading', 'json', 'select', 'time', 'datetime', ''],
    'excludes': ['tkinter'],
    'include_files': [(r"C:\Python34\Lib\site-packages\PyQt4\plugins\sqldrivers","sqldrivers"),('changelog', 'changelog.txt')]}

base = None

if sys.platform == 'win32':
    base = 'Win32GUI'
    # base = 'console'

setup(  name = 'EAMI',
        version = __version__,
        description = "Etcher's Automated Mod Installer",
        options = {'build_exe': build_exe_options},
        executables = [
            Executable('eami.py',
                       base=base,
                       icon='./logos/eami.ico',
                       # targetDir='build/EAMIv{}'.format(__version__)
            )],
        requires=['PyQt4'])