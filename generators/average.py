# -*- coding: utf-8 -*-
# @Author: ckochman
# @Date:   2017-05-04 16:47:30
# @Last Modified by:   ckochman
# @Last Modified time: 2017-05-04 17:29:15

from started import started

@started
def average():
    """ generator that holds a rolling average """
    count = 0.0
    total = generators.sum()
    i=0
    while 1:
        i = yield (total.send(i)*1.0/count if count else 0)
        count += 1
