#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Cody Kochmann
# @Date:   2017-09-09
# @Last Modified by:   Cody Kochmann

from collections import deque


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
    # yield the windows
    for i in iterable:
        yield tuple(d)
        d.append(i)
    yield tuple(d)
