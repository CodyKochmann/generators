# -*- coding: utf-8 -*-
# @Author: Cody Kochmann
# @Date:   2018-01-24 11:52:06
# @Last Modified 2018-01-24
# @Last Modified time: 2018-01-24 11:57:27

from strict_functions import noglobals

@noglobals
def chunk_on(pipeline, new_chunk_signal):
    ''' split the stream into seperate chunks based on a new chunk signal '''
    out = []
    for i in pipeline:
        if new_chunk_signal(i) and len(out): # if new chunk start detected
            yield out
            out = []
        out.append(i)
    # after looping, if there is anything in out, yield that too
    if len(out):
        yield out

if __name__ == '__main__':
    for i in chunk_on(range(30), lambda i:i%3==0):
        print(i)

