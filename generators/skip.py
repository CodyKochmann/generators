# -*- coding: utf-8 -*-
# @Author: Cody Kochmann
# @Date:   2018-02-17 10:40:09
# @Last Modified by:   Cody Kochmann
# @Last Modified time: 2018-02-17 11:59:23

from itertools import islice

def skip(pipe, how_many=1):
    ''' this is a helper function that allows you to skip x number of items
        in a pipe. its basically the same is running next() on a generator
        multiple times to move down the generator's stream.

        The return value is the pipe that has now skipped x number of steps
    '''
    for _ in islice(pipe, how_many):
        pass
    return pipe

if __name__ == '__main__':
    g = iter(range(10))
    print(next(g))
    print(next(g))
    print(next(g))
    skip(g,3)
    print(next(g))
    print(next(g))
    print(next(g))

