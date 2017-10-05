# -*- coding: utf-8 -*-
# @Author: Cody Kochmann
# @Date:   2017-09-09 09:15:15
# @Last Modified 2017-10-05
# @Last Modified time: 2017-09-09 09:15:33


def iter_kv(d):
    ''' iterate through massive dictionaries without the slowdown and memory usage of dict.items '''
    for k in d:
        yield k, d[k]
