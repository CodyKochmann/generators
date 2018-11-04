#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Cody Kochmann
# @Date:   2017-09-09
# @Last Modified 2017-10-17

try:
    from itertools import zip_longest
except ImportError:
    from itertools import izip_longest as zip_longest, imap as map
else:
    map = map

from strict_functions import strict_globals
from chunk_on import chunk_on
from apply_to_last import apply_to_last
from iterable import iterable

@strict_globals(zip_longest=zip_longest, apply_to_last=apply_to_last, chunk_on=chunk_on, iterable=iterable, map=map)
def chunks(stream, chunk_size, output_type=tuple):
    ''' returns chunks of a stream '''
    assert iterable(stream), 'chunks needs stream to be iterable'
    assert (isinstance(chunk_size, int) and chunk_size > 0) or callable(chunk_size), 'chunks needs chunk_size to be a positive int or callable'
    assert callable(output_type), 'chunks needs output_type to be callable'
    if callable(chunk_size):
        ''' chunk_size is acting as a separator function '''
        for chunk in chunk_on(stream, chunk_size, output_type):
            yield chunk
    else:
        it = iter(stream)
        marker = object()
        iters = [it] * chunk_size
        pipeline = apply_to_last(
           zip_longest(*iters, fillvalue=marker),
           lambda last_chunk: tuple(i for i in last_chunk if i is not marker)
        )
        if output_type is not tuple:
            pipeline = map(output_type, pipeline)
        for chunk in pipeline:
            yield chunk

del zip_longest
del apply_to_last
del chunk_on
del map
del strict_globals
