# -*- coding: utf-8 -*-
# @Author: ckochman
# @Date:   2017-05-04 18:03:35
# @Last Modified by:   ckochman
# @Last Modified time: 2017-05-04 18:03:44

def unfork(g):
    """ returns a generator with one output at a time if
        multiple outputs are coming out of the given """
    for i in g:
        for x in i:
            yield x
