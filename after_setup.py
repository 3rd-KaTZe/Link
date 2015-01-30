# coding=utf-8
__author__ = 'etcher3rd'

from os import rename, remove, chdir, walk
from os.path import exists, join, abspath
from shutil import rmtree, move
from helo_link import __version__
from zipfile import ZipFile, ZIP_LZMA
from subprocess import Popen

src = './build/exe.win32-3.4'
z = abspath('./build/KATZE_LINK_{}.zip'.format(__version__))

if exists(z):
    remove(z)

chdir(src)

# Popen("7z a -t7z -mx9 {} ./*".format(z)).wait()


with ZipFile(z, mode="w", compression=ZIP_LZMA) as zip_file:
    # logger.debug("WorkerModBuilder - énumération des fichiers à compresser")
    file_count = 0
    current = 1
    for root, dirs, files in walk('.'):
        for _ in files:
            file_count += 1
    # logger.debug("WorkerModBuilder - nombre de fichier à comresser: {}".format(file_count))
    for root, dirs, files in walk('.'):
        for file in files:
            # progress.update("Compression du fichier {}/{}".format(current, file_count))
            # logger.debug("WorkerModBuilder - compression du fichier: {}".format(join(root, file)))
            zip_file.write(join(root, file))
            current += 1
    # logger.info("WorkerModBuilder - compression terminée, fermeture du fichier ZIP")
    # progress.update("Compression terminée")


# tgt = '../build/{}'.format(z)
# if exists(tgt):
#     remove(tgt)
# move(z, '../build')
# chdir('..')
# rmtree(src)

# ftp = FTP()
# ftp.connect('ftp.3rd-wing.net')
# ftp.login(user="ownagete-pil", passwd="BordAile")
# ftp.cwd(Config.defaults['new_eami_version_location'])
# with open(z, mode='rb') as f:
#     ftp.storbinary('STOR {}'.format('EAMIv{}.7z'.format(__version__)), f, blocksize=1024)