# -*- coding: utf-8 -*-
# @Author: Cody Kochmann
# @Date:   2017-09-09 14:58:43
# @Last Modified by:   Cody Kochmann
# @Last Modified time: 2017-09-09 14:58:50

def chain(*a):
    """itertools.chain, just better"""
    for g in a:
        if hasattr(g, '__iter__'):
            # iterate through if its iterable
            for i in g:
                yield i
        else:
            # just yield the whole thing if its not
            yield g
