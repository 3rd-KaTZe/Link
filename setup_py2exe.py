# coding=utf-8
__author__ = 'etcher3rd'

from distutils.core import setup
from helo_link import __version__
import py2exe


setup(
    requires=['requests'],
    name="KAtzeLink v{}".format(__version__),
    data_files=[
        ('', ['./config_Helo-Link.csv', 'z_Data_Dico.csv']),

    ],
    console=[
        {
            'script': 'helo_link.py',
        }
    ],
    options={
        'py2exe': {
        }
    },
)
