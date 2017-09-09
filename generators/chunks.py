#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Cody Kochmann
# @Date:   2017-09-09
# @Last Modified by:   Cody Kochmann

from collections import deque


def chunks(iterable, chunk_size, output_type=tuple):
    ''' returns chunks of an iterable '''
    chunk = deque(maxlen=chunk_size)
    for i in iterable:
        chunk.append(i)
        if len(chunk) == chunk_size:
            yield output_type(chunk)
            chunk.clear()
    if len(chunk):
        yield output_type(chunk)
