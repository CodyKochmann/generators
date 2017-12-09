# -*- coding: utf-8 -*-
# @Author: ckochman
# @Date:   2017-05-04 18:03:35
# @Last Modified by:   Cody Kochmann
# @Last Modified time: 2017-12-09 13:33:14

from strict_functions import noglobals

@noglobals
def unfork(g):
    """ returns a generator with one output at a time if
        multiple outputs are coming out of the given """
    for i in g:
        for x in i:
            yield x

del noglobals

if __name__ == '__main__':
    g = ((i for i in range(10)) for x in range(20))
    for i in unfork(g):
        print(i)
