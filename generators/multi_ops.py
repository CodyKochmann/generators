# -*- coding: utf-8 -*-
# @Author: ckochman
# @Date:   2017-05-04 18:04:39
# @Last Modified by:   ckochman
# @Last Modified time: 2017-05-05 11:53:06

def multi_ops(g, *f):
    """ fork a generator with multiple operations/functions """
    assert all(callable(func) for func in f), 'multi_ops can only apply functions to the first argument'
    for i in g:
        if len(f) > 1:
            yield tuple(func(i) for func in f)
        elif len(f) == 1:
            yield f[0](i)

if __name__ == '__main__':
    # example usage below
    tmp = [1,2,3,4,5]
    gen = multi_ops(
        tmp,
        int,
        float,
        str,
        repr,
        bool
    )
    for i in gen:
        print(i)
