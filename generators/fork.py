# -*- coding: utf-8 -*-
# @Author: ckochman
# @Date:   2017-05-04 18:03:54
# @Last Modified by:   Cody Kochmann
# @Last Modified time: 2017-12-09 10:47:42

from strict_functions import noglobals

@noglobals
def fork(iterate, forks=2):
    """ use this to fork a generator """
    return ((i,)*forks for i in iterate)

del noglobals

if __name__ == '__main__':
    g = fork(range(10), 5)
    for i in g:
        print(i)
