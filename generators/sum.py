# -*- coding: utf-8 -*-
# @Author: ckochman
# @Date:   2017-05-04 16:44:45
# @Last Modified by:   ckochman
# @Last Modified time: 2017-05-04 16:44:59

from started import started

@started
def sum():
    "generator that holds a sum"
    total = 0
    while 1:
        total += yield total
