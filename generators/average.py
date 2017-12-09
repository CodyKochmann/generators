# -*- coding: utf-8 -*-
# @Author: ckochman
# @Date:   2017-05-04 16:47:30
# @Last Modified by:   Cody Kochmann
# @Last Modified time: 2017-12-09 10:26:44

from started import started
from total import total
from strict_functions import strict_globals


@started
@strict_globals(total=total)
def average():
    """ generator that holds a rolling average """
    count = 0
    total = total()
    i=0
    while 1:
        i = yield ((total.send(i)*1.0)/count if count else 0)
        count += 1

del total
del started
del strict_globals
