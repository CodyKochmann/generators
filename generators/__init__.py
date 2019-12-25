#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
import os.path

sys.path.append(os.path.dirname(__file__))

from performance_tools import runs_per_second as rps

from all_subslices import all_subslices
from all_substrings import all_substrings
from alternator import alternator
from average import average
from apply_to_last import apply_to_last
from chain import chain
from chunk_on import chunk_on
from chunks import chunks
from consume import consume
from counter import counter
from early_warning import early_warning
from every_other import every_other
from first import first
from fork import fork
from itemgetter import itemgetter
from iter_csv import iter_csv
from iter_kv import iter_kv
from iterable import iterable
from just import just
from last import last
from loop import loop
from map import map
from map_parallel import map_parallel, map_multicore, map_multithread
from multi_ops import multi_ops
from peekable import peekable
from read import read
from remember import remember
from repeater import repeater
from reverse import reverse
from side_task import side_task
from skip import skip
from skip_first import skip_first
from skip_last import skip_last
from split import split
from started import started
from switch import switch
from tee import tee
from timed_pipe import timed_pipe
from timer import timer
from total import total
from unfork import unfork
from uniq import uniq
from window import window

import inline_tools
import performance_tools

# this prevents recursive importing
try:
    from Generator import Generator
    G = Generator
except ImportError:
    pass

# attempt to suck in all the tests so tests can be ran with:
#   python -m unittest generators
try:
    from tests import *
except:
    pass

#import unittest
#unittest.defaultTestLoader.discover(os.path.join(os.path.dirname(__file__), 'tests'))

#    print('importing Generator')
#else:
#    print('skipping Generator')

__all__ = ['G', 'Generator', 'apply_to_last', 'all_subslices', 'all_substrings', 'alternator', 'average', 'chain', 'chunk_on', 'chunks', 'consume', 'counter', 'early_warning', 'every_other', 'first', 'fork', 'itemgetter', 'iter_csv', 'iter_kv', 'iterable', 'just', 'last', 'loop', 'map', 'multi_ops', 'peekable', 'read', 'remember', 'repeater', 'side_task', 'skip', 'skip_first', 'skip_last', 'split', 'started', 'tee', 'timed_pipe', 'timer', 'total', 'unfork', 'uniq', 'window', 'inline_tools', 'performance_tools']

sys.path.remove(os.path.dirname(__file__))

del sys
del os
