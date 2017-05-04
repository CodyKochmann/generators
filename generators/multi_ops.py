# -*- coding: utf-8 -*-
# @Author: ckochman
# @Date:   2017-05-04 18:04:39
# @Last Modified by:   ckochman
# @Last Modified time: 2017-05-04 18:05:28

def multi_ops(g, *f):
    """ fork a generator with multiple operations being
        ran on its values """
    for i in g:
        if len(f)>1:
            yield tuple(func(i) for func in f)
        else:
            yield f[0](i)
