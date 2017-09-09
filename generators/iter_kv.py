# -*- coding: utf-8 -*-
# @Author: Cody Kochmann
# @Date:   2017-09-09 09:15:15
# @Last Modified by:   Cody Kochmann
# @Last Modified time: 2017-09-09 09:15:33


def iter_kv(d):
    ''' does what dict.items() does, without wasting memory '''
    for k in d:
        yield k, d[k]
