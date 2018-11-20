# -*- coding: utf-8 -*-
# @Author: Cody Kochmann
# @Date:   2018-01-24 11:52:06
# @Last Modified 2018-01-24
# @Last Modified time: 2018-01-24 11:57:27

from collections import deque
from strict_functions import strict_globals
from iterable import iterable

@strict_globals(deque=deque, iterable=iterable)
def chunk_on(pipeline, new_chunk_signal, output_type=tuple):
    ''' split the stream into seperate chunks based on a new chunk signal '''
    assert iterable(pipeline), 'chunks needs pipeline to be iterable'
    assert callable(new_chunk_signal), 'chunks needs new_chunk_signal to be callable'
    assert callable(output_type), 'chunks needs output_type to be callable'
    
    out = deque()
    for i in pipeline:
        if new_chunk_signal(i) and len(out): # if new chunk start detected
            yield output_type(out)
            out.clear()
        out.append(i)
    # after looping, if there is anything in out, yield that too
    if len(out):
        yield output_type(out)
