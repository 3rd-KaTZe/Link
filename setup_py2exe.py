# coding=utf-8
__author__ = 'etcher3rd'


from distutils.core import setup
from helo_link import __version__
import py2exe


setup(
    requires=['PyQt5'],
    name="KatzeLink v{}".format(__version__),
    data_files=[
        ('', ['./config_Helo-Link.csv', 'z_Data_Dico.csv',]),
        ('platforms', [r'C:\Python34\Lib\site-packages\PyQt5\plugins\platforms\qwindows.dll'])

    ],
    windows=[
        {
            'script': 'helo_link.py',
        }
    ],
    options={
        'py2exe': {
            # 'packages': ['win32com'],
            'includes': ['sip']
        }
    },
)
