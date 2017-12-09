# -*- coding: utf-8 -*-
# @Author: ckochman
# @Date:   2017-10-05 16:47:30
# @Last Modified 2017-10-05
# @Last Modified time: 2017-12-09 13:21:35

from __future__ import print_function
del print_function

import sys
import os.path

sys.path.append(os.path.dirname(__file__))

del sys
del os

from iterable import iterable
from map import map

from strict_functions import strict_globals

@strict_globals(map=map, iterable=iterable)
def side_task(pipe, *side_jobs):
    ''' allows you to run a function in a pipeline without affecting the data '''
    # validate the input
    assert iterable(pipe), 'side_task needs the first argument to be iterable'
    for sj in side_jobs:
        assert callable(sj), 'all side_jobs need to be functions, not {}'.format(sj)
    # add a pass through function to side_jobs
    side_jobs = (lambda i:i ,) + side_jobs
    # run the pipeline
    for i in map(pipe, *side_jobs):
        yield i[0]

del iterable, strict_globals

if __name__ == '__main__':
    from time import time as ts
    from collections import defaultdict
    from window import window
    from iter_kv import iter_kv

    even_odd_sums = defaultdict(float)
    set_even_odd = even_odd_sums.__setitem__

    # this builds a pipeline of tuples as (index, timestamp)
    pipeline = map(range(30), lambda i:i, lambda i:ts())
    # this finds the difference between each timestamp
    pipeline = map(
        window(pipeline, 2),
        lambda i:i[1][0], # the last key
        lambda i:i[1][1]-i[0][1]
    )
    # add the time to the correct slot in even_odd_sums
    pipeline = side_task(
        pipeline,
        lambda i:set_even_odd(i[0]%2, even_odd_sums[i[0]%2]+i[1])
    )
    # this runs a side job without changing the flow
    pipeline = side_task(pipeline, print)

    # run the generator
    for i in pipeline:
        pass
    # show the results in even_odd_sums
    for i in iter_kv(even_odd_sums):
        print(i)
