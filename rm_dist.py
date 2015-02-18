# coding=utf-8
__author__ = 'etcher3rd'

from shutil import rmtree
from os.path import abspath, exists

try:
    if exists('./build/exe.win32-3.4'):
        rmtree('./build/exe.win32-3.4')
except:
    print("Impossible de supprimer le dossier ./exe.win32-3.4")
    exit(0)