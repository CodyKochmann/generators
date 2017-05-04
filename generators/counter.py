# -*- coding: utf-8 -*-
# @Author: ckochman
# @Date:   2017-05-04 16:45:16
# @Last Modified by:   ckochman
# @Last Modified time: 2017-05-04 16:45:29

from started import started

@started
def counter():
    "generator that holds a sum"
    c = 0
    while 1:
        yield c
        c += 1
