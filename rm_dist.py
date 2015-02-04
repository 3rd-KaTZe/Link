# coding=utf-8
__author__ = 'etcher3rd'

from shutil import rmtree

try:
    rmtree('./dist')
except:
    print("Impossible de supprimer le dossier ./dist")
    exit(0)