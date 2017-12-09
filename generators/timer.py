# -*- coding: utf-8 -*-
# @Author: ckochman
# @Date:   2017-05-04 16:48:03
# @Last Modified by:   Cody Kochmann
# @Last Modified time: 2017-12-09 13:29:27

from started import started
from timeit import default_timer as ts
from strict_functions import strict_globals


@started
@strict_globals(ts=ts)
def timer():
    """ generator that tracks time """
    start_time = ts()
    while 1:
        yield ts()-start_time

del ts, started, strict_globals

if __name__ == '__main__':
    # some example usage
    count = 10**6
    t = timer()
    ( i for i in range(count) )
    print(next(t))
    { i for i in range(count) }
    print(next(t))
    { i:i for i in range(count) }
    print(next(t))
    tuple( i for i in range(count) )
    print(next(t))
    [ i for i in range(count) ]
    print(next(t))
