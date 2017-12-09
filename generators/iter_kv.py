# -*- coding: utf-8 -*-
# @Author: Cody Kochmann
# @Date:   2017-09-09 09:15:15
# @Last Modified 2017-10-05
# @Last Modified time: 2017-12-09 11:20:06

from strict_functions import noglobals


@noglobals
def iter_kv(d):
    ''' This iterates through massive dictionaries without the slowdown and memory usage of
    dict.items. Python 3 does provide an iterable dict.items but using this instead gives you
    uniform behavior in both versions of python '''
    for k in d:
        yield k, d[k]

del noglobals

if __name__ == '__main__':
    d = {i:i+3 for i in range(20)}
    for k,v in iter_kv(d):
        print(k,v)
