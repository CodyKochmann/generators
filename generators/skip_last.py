# -*- coding: utf-8 -*-
# @Author: Cody Kochmann
# @Date:   2018-02-17 10:42:38
# @Last Modified by:   Cody Kochmann
# @Last Modified time: 2018-02-17 11:53:30

from window import window
from collections import deque
from itertools import islice

def skip_last(pipe, how_many=1):
    pipe = iter(pipe)
    d = deque(islice(pipe, how_many), maxlen=how_many+1)
    for _ in map(d.append, pipe):
        yield d.popleft()

if __name__ == '__main__':
    l = list(range(10))
    print(l)
    for i in range(12):
        print(i, '-', list(skip_last(l, i)))
