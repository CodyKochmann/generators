# -*- coding: utf-8 -*-
# @Author: Cody Kochmann
# @Date:   2018-01-24 11:52:06
# @Last Modified 2018-01-24
# @Last Modified time: 2020-04-19 10:35:07

from itertools import groupby, chain
from .iterable import iterable

def chunk_on(pipeline, new_chunk_signal, output_type=tuple):
    ''' split the stream into seperate chunks based on a new chunk signal '''
    assert iterable(pipeline), 'chunks needs pipeline to be iterable'
    assert callable(new_chunk_signal), 'chunks needs new_chunk_signal to be callable'
    assert callable(output_type), 'chunks needs output_type to be callable'
    
    holder = []
    
    for signal, group in groupby(pipeline, new_chunk_signal):
        if signal:
            for i in group:
                holder = [i]
                break
            for i in group:
                yield output_type(holder)
                holder = [i]
        else:
            yield output_type(
                chain(
                    holder, 
                    group
                )
            )
            holder = []
    if holder:
        yield output_type(holder)
        