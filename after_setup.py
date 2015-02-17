# coding=utf-8
__author__ = 'etcher3rd'

from os import chdir, walk
from os.path import exists, join, abspath
from main import __version__
from zipfile import ZipFile, ZIP_LZMA
from subprocess import call
from time import  sleep

chdir('./build')

z_local = './KaTZeLinkV2_{}.zip'.format(__version__)
z = abspath(z_local)

chdir('./exe.win32-3.4')

with ZipFile(z, mode="w", compression=ZIP_LZMA) as zip_file:
    for root, dirs, files in walk('.'):
        for file in files:
            zip_file.write(join(root, file))

chdir('..')

print('N\'OUBLIE PAS DE PUSHER ESPECE DE SINGE !!!')
name = input('name: ')
desc = input('description: ')

if not call('github-release release --user 3rd-KaTZe --repo Link --tag {} --name "{}" --description "{}"'.format(
        __version__, name, desc)) == 0:
    call('github-release edit -u 3rd-KaTZe -r Link -t {} -n "{}" -d "{}"'.format(__version__, name, desc))

sleep(3)
print('uploading {}'.format(z_local))
call('github-release upload -u 3rd-KaTZe -r Link --tag {} -n "KaTZeLink_{}.7z" -f "{}"'
     .format(__version__, __version__, z_local))
