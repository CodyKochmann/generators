# -*- coding: utf-8 -*-
# @Author: ckochman
# @Date:   2017-05-04 16:48:03
# @Last Modified by:   ckochman
# @Last Modified time: 2017-05-05 11:35:52

from started import started
from time import time

@started
def timer():
    """ generator that tracks time """
    start_time = time()
    while 1:
        yield time()-start_time

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
