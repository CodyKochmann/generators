# -*- coding: utf-8 -*-
# @Author: Cody Kochmann
# @Date:   2018-02-17 10:42:27
# @Last Modified by:   Cody Kochmann
# @Last Modified time: 2018-02-17 11:26:24

from collections import deque

def last(pipe, items=1):
    ''' this function simply returns the last item in an iterable '''
    if items == 1:
        tmp=None
        for i in pipe:
            tmp=i
        return tmp
    else:
        return tuple(deque(pipe, maxlen=items))

if __name__ == '__main__':
    g = iter(range(10))
    print(last(g))
    g = iter(range(20))
    print(last(g, 5))
