# -*- coding: utf-8 -*-
# @Author: ckochman
# @Date:   2017-05-04 16:44:45
# @Last Modified by:   Cody Kochmann
# @Last Modified time: 2017-12-09 13:31:32

from started import started
from strict_functions import noglobals

@started
@noglobals
def total():
    "generator that holds a total"
    total = 0
    while 1:
        total += yield total

del started, noglobals

if __name__ == '__main__':
    g=total()
    for i in range(10):
        print(g.send(i))
