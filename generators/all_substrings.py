#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Cody Kochmann
# @Date:   2017-09-09
# @Last Modified by:   Cody Kochmann

from functools import partial
from window import window


def all_substrings(s):
    ''' yields all substrings of a string '''
    join = partial(''.join)
    for i in range(1, len(s) + 1):
        for sub in window(s, i):
            yield join(sub)
