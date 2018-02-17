# -*- coding: utf-8 -*-
# @Author: Cody Kochmann
# @Date:   2018-02-17 10:41:53
# @Last Modified by:   Cody Kochmann
# @Last Modified time: 2018-02-17 11:02:53

def consume(pipe, how_many=0):
    for _ in (pipe if how_many==0 else islice(pipe, 0, how_many)):
        pass


if __name__ == '__main__':
    g=iter(range(30))
    consume(g)
    try:
        print(next(g))
    except StopIteration:
        print('g is now empty')
