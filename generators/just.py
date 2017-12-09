# -*- coding: utf-8 -*-
# @Author: Cody Kochmann
# @Date:   2017-10-12 11:28:15
# @Last Modified 2017-10-12
# @Last Modified time: 2017-12-09 11:23:23

from itertools import cycle
from strict_functions import strict_globals

@strict_globals(cycle=cycle)
def just(*args):
    ''' this works as an infinite loop that yields
        the given argument(s) over and over
    '''
    assert len(args) >= 1, 'generators.just needs at least one arg'

    if len(args) == 1: # if only one arg is given
        try:
            # try to cycle in a set for iteration speedup
            return cycle(set(args))
        except:
            # revert to cycling args as a tuple
            return cycle(args)
    else:
        return cycle({args})

del cycle, strict_globals

if __name__ == '__main__':
    g = just(5)
    for i in range(10):
        print(next(g))
    g = just(5,6,7)
    for i in range(10):
        print(next(g))
    g = just(list(range(3)))
    for i in range(10):
        print(next(g))
