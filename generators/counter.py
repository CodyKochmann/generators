# -*- coding: utf-8 -*-
# @Author: ckochman
# @Date:   2017-05-04 16:45:16
# @Last Modified by:   Cody Kochmann
# @Last Modified time: 2017-12-09 10:37:37

from started import started
from strict_functions import noglobals


@started
@noglobals
def counter():
    "generator that holds a sum"
    c = 0
    while 1:
        yield c
        c += 1


del started
del noglobals

if __name__ == '__main__':
    g = counter()
    for i in range(10):
        print(next(g))
