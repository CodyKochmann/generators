# -*- coding: utf-8 -*-
# @Author: ckochman
# @Date:   2017-05-04 17:06:34
# @Last Modified by:   Cody Kochmann
# @Last Modified time: 2017-05-05 16:34:43

from os import listdir
from generators import read_file

readme_header = """
# generators
Where all of my generator tricks are collected!
"""

def get_source(path):
    for line in read_file(path):
        if '__name__' in line and '__main__' in line:
            break
        if not line.startswith("#") or not len(line.strip()):
            yield line

# list the files
gen = ('generators/{}'.format(i) for i in listdir('generators'))
# filter out __init__.py
gen = (i for i in gen if not i.endswith('__init__.py'))
# filter out pyc's
gen = (i for i in gen if not i.endswith('.pyc'))
# read the lines of each file
gen = (((x for x in get_source(i)),i) for i in gen)

with open('README.md', 'w') as readme:
    readme.write(readme_header+'\n')
    for f, path in gen:
        readme.write('### '+path.split('/')[1]+'\n```python')
        readme.writelines(f)
        readme.write('```\n\n')

with open('README.md') as f:
    print(f.read())
