#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Cody Kochmann
# @Date:   2017-10-12 11:24:42
# @Last Modified 2017-10-12
# @Last Modified time: 2017-10-12 11:36:59

from itertools import cycle

def loop():
    '''
    use this for infinite iterations with

        for _ in loop():

    instead of:

        while True:

    to get a free speedup in loops.
    '''
    return cycle({0})

if __name__ == '__main__':
    c = 10
    for _ in loop():
        if c == 0:
            break
        else:
            print(c)
            c -= 1
