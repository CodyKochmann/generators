#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Cody Kochmann
# @Date:   2017-09-09
# @Last Modified 2017-10-17

from collections import deque
from strict_functions import strict_globals


@strict_globals(deque=deque)
def chunks(stream, chunk_size, output_type=tuple):
    ''' returns chunks of a stream '''
    if callable(chunk_size):
        ''' chunk_size is acting as a separator function '''
        seperator = chunk_size
        chunk = deque()
        for i in stream:
            if seperator(i) and len(chunk):
                yield output_type(chunk)
                chunk.clear()
            chunk.append(i)
    else:
        chunk = deque(maxlen=chunk_size)
        for i in stream:
            chunk.append(i)
            if len(chunk) == chunk_size:
                yield output_type(chunk)
                chunk.clear()
    if len(chunk):
        yield output_type(chunk)

del deque
del strict_globals

if __name__ == '__main__':
    l = list(range(30))
    print(list(chunks(l, 2)))
    print(list(chunks(l, 15)))
    print(list(chunks(l, 20)))
    print(list(chunks(l, lambda i:i==15)))
    print(list(chunks(l, lambda i:i%5==0)))
    print(list(chunks(l, lambda i:str(i).startswith('1'))))

