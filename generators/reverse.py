# -*- coding: utf-8 -*-
# @Author: Cody Kochmann
# @Date:   2018-03-10 09:10:41
# @Last Modified by:   Cody Kochmann
# @Last Modified time: 2018-03-10 09:14:03

def reverse(pipe):
    ''' this has the same funcitonality as builtins.reversed(), except this
        doesnt complain about non-reversable things. If you didnt know already,
        a generator needs to fully run in order to be reversed.
    '''
    for i in reversed(list(pipe)):
        yield i

if __name__ == '__main__':
    print(reverse(iter(range(20))))
    print(list(reverse(iter(range(20)))))
