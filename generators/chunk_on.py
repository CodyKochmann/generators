# -*- coding: utf-8 -*-
# @Author: Cody Kochmann
# @Date:   2018-01-24 11:52:06
# @Last Modified 2018-01-24
# @Last Modified time: 2018-01-24 11:57:27

from collections import deque
from strict_functions import strict_globals

@strict_globals(deque=deque)
def chunk_on(pipeline, new_chunk_signal, output_type=tuple):
    ''' split the stream into seperate chunks based on a new chunk signal '''
    out = deque()
    for i in pipeline:
        if new_chunk_signal(i) and len(out): # if new chunk start detected
            yield output_type(out)
            out.clear()
        out.append(i)
    # after looping, if there is anything in out, yield that too
    if len(out):
        yield output_type(out)

if __name__ == '__main__':
    for i in chunk_on(range(30), lambda i:i%3==0):
        print(i)

    l = list(range(30))
    print(list(chunk_on(l, lambda i:i==15)))
    print(list(chunk_on(l, lambda i:i%5==0)))
    print(list(chunk_on(l, lambda i:str(i).startswith('1'))))
