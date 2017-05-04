# -*- coding: utf-8 -*-
# @Author: ckochman
# @Date:   2017-05-04 16:44:45
# @Last Modified by:   ckochman
# @Last Modified time: 2017-05-04 17:13:47

from started import started

@started
def total():
    "generator that holds a total"
    total = 0
    while 1:
        total += yield total
