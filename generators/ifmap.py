# -*- coding: utf-8 -*-
# @Author: CodyKochmann
# @Date:   2020-04-19 10:43:11
# @Last Modified by:   CodyKochmann
# @Last Modified time: 2020-04-19 10:43:56

from .iterable import iterable

def ifmap(pipe, condition, map_function):
    ''' applies a map operation to items in a pipe
        IF the provided condition returns true
        otherwise, the item is passed through
    '''
    assert iterable(pipe), pipe
    assert callable(condition), condition
    assert callable(map_function), map_function
    
    for i in pipe:
        yield map_function(i) if condition(i) else i