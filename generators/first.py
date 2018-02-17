# -*- coding: utf-8 -*-
# @Author: Cody Kochmann
# @Date:   2018-02-17 10:42:02
# @Last Modified by:   Cody Kochmann
# @Last Modified time: 2018-02-17 10:59:27

from itertools import islice

def first(pipe, items=1):
    ''' first is essentially the next() function except it's second argument
        determines how many of the first items you want. If items is more than
        1 the output is an islice of the generator. If items is 1, the first
        item is returned
    '''
    pipe = iter(pipe)
    return next(pipe) if items == 1 else islice(pipe, 0, items)

if __name__ == '__main__':
    g = iter(range(10))
    print(next(g))
    print(first(g))
    print(list(first(g, 5)))
