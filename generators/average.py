# -*- coding: utf-8 -*-
# @Author: ckochman
# @Date:   2017-05-04 16:47:30
# @Last Modified by:   Cody Kochmann
# @Last Modified time: 2017-09-09 09:55:16

from started import started
from total import total


@started
def average():
    """ generator that holds a rolling average """
    count = 0
    total = total()
    i=0
    while 1:
        i = yield ((total.send(i)*1.0)/count if count else 0)
        count += 1
