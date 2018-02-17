# -*- coding: utf-8 -*-
# @Author: Cody Kochmann
# @Date:   2018-02-17 14:26:22
# @Last Modified by:   Cody Kochmann
# @Last Modified time: 2018-02-17 14:38:45

def repeater(pipe, how_many=2):
    ''' this function repeats each value in the pipeline however many times you need '''
    r = range(how_many)
    for i in pipe:
        for _ in r:
            yield i

if __name__ == '__main__':
    l = list(range(10))
    print(l)
    print(list(repeater(l)))
    print(list(repeater(l, 3)))
