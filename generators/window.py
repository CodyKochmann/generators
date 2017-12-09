#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Cody Kochmann
# @Date:   2017-09-09
# @Last Modified by:   Cody Kochmann

from collections import deque
from strict_functions import strict_globals

@strict_globals(deque=deque)
def window(iterable, size):
    ''' yields wondows of a given size '''
    d = deque(maxlen=size)
    # normalize iterable into a generator
    iterable = (i for i in iterable)
    # fill d until full
    for i in iterable:
        d.append(i)
        if len(d) == size:
            break
    if len(d) == d.maxlen:
        # yield the windows
        for i in iterable:
            yield tuple(d)
            d.append(i)
        yield tuple(d)

del deque, strict_globals

if __name__ == '__main__':
    g = window(range(20), 3)
    for i in g:
        print(i)
