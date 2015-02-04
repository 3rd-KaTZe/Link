# coding=utf-8
__author__ = 'etcher3rd'

from os import chdir, walk
from os.path import exists, join, abspath
from helo_link import __version__
from zipfile import ZipFile, ZIP_LZMA
from os import mkdir
from subprocess import call
from time import sleep

src = './dist'
if not exists('./build'):
    mkdir('./build')

z_local = './build/KaTZeLink{}.zip'.format(__version__)
z = abspath(z_local)

chdir(src)


with ZipFile(z, mode="w", compression=ZIP_LZMA) as zip_file:
    for root, dirs, files in walk('.'):
        for file in files:
            zip_file.write(join(root, file))

chdir('..')

name = input('name: ')
desc = input('description: ')

if not call('github-release release --user 3rd-KaTZe --repo Link --tag {} --name "{}" --description "{}"'.format(
        __version__, name, desc)) == 0:
    call('github-release edit -u 3rd-KaTZe -r Link -t {} -n "{}" -d "{}"'.format(__version__, name, desc))

sleep(3)
print('uploading {}'.format(z_local))
call('github-release upload -u 3rd-KaTZe -r Link --tag {} -n "KaTZeLink_{}.zip" -f "{}"'
     .format(__version__, __version__, z_local))
