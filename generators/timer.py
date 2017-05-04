# -*- coding: utf-8 -*-
# @Author: ckochman
# @Date:   2017-05-04 16:48:03
# @Last Modified by:   ckochman
# @Last Modified time: 2017-05-04 16:48:14

from started import started

@started
def timer():
    """ generator that tracks time """
    start_time = time()
    previous = start_time
    while 1:
        yield time()-start_time
