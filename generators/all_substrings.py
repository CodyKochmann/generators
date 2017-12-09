#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Cody Kochmann
# @Date:   2017-09-09
# @Last Modified by:   Cody Kochmann

from window import window
from strict_functions import strict_globals


@strict_globals(window=window)
def all_substrings(s):
    ''' yields all substrings of a string '''
    join = ''.join
    for i in range(1, len(s) + 1):
        for sub in window(s, i):
            yield join(sub)

del window
del strict_globals
