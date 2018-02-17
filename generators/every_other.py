# -*- coding: utf-8 -*-
# @Author: Cody Kochmann
# @Date:   2018-02-17 10:40:40
# @Last Modified by:   Cody Kochmann
# @Last Modified time: 2018-02-17 14:38:04

from itertools import cycle
from repeater import repeater

def every_other(pipe, how_many=1):
    ''' feeding this function a pipe yields every other (or how ever many)
        objects you want at a time.
    '''
    for i,x in zip(pipe, cycle(repeater([True,False], how_many))):
        if x:
            yield i

if __name__ == '__main__':
    l = list(range(30))
    print(l)
    print(list(every_other(l)))
    print(list(every_other(l, 10)))
