# coding=utf-8
__author__ = 'etcher3rd'

from os import walk, chdir
from subprocess import Popen

chdir(r'./ui')

p = Popen("build_ui.bat")
stdout, stderr = p.communicate()
print(stderr)

for root, dirs, files in walk('.'):
    for file in files:
        if file[-3:] == '.py' and not file in ['__init__.py']:
            o = []
            with open(file) as f:
                lines = f.readlines()
            for l in lines:
                if l[0] == "#":
                    continue
                o.append(l)
            with open(file, "w") as f:
                f.writelines(o)

chdir('..')