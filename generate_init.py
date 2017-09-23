# -*- coding: utf-8 -*-
# @Author: Cody Kochmann
# @Date:   2017-09-09 10:02:28
# @Last Modified by:   Cody Kochmann
# @Last Modified time: 2017-09-09 10:36:07

header = '''#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
import os.path

sys.path.append(os.path.dirname(__file__))

sys.path.append(os.path.join(os.path.dirname(__file__), 'inline_tools'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'performance_tools'))

import inline_tools
import performance_tools

'''
import sys
import os.path
from os import listdir
from functools import partial

script_path = os.path.dirname(__file__)
init_path = os.path.join(script_path, 'generators')

# this builds the full path to a given file in generators
path_of = partial(os.path.join, init_path)

# get all the python files from init_path
gen = (i for i in listdir(init_path) if i.endswith('.py'))
# filter out __init__.py
gen = (i for i in gen if '__init__.py' not in i)
# verify that they all have functions that match the file name
gen = (i for i in gen
       if 'def {}('.format(i[:-3]) in open(path_of(i), 'r').read())
# trim off the .pys
gen = (i[:-3] for i in gen)

# serves as the all that will be injected into __init__
__all__ = ['inline_tools', 'performance_tools']

# rebuild the __init__
with open(path_of('__init__.py'), 'w') as f:
    print('writing header')
    f.write(header)
    for i in gen:
        __all__.append(i)
        print('adding import for', i)
        f.write('from {i:} import {i:}\n'.format(i=i))
    print('adding __all__')
    f.write('\n__all__ = {}\n'.format(__all__))

print('done')
