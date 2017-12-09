# -*- coding: utf-8 -*-
# @Author: ckochman
# @Date:   2017-05-04 18:04:39
# @Last Modified by:   Cody Kochmann
# @Last Modified time: 2017-12-09 11:30:26

from strict_functions import noglobals

@noglobals
def multi_ops(data_stream, *funcs):
    """ fork a generator with multiple operations/functions

        data_stream  -  an iterable data structure (ie: list/generator/tuple)
        funcs        -  every function that will be applied to the data_stream """

    assert all(callable(func) for func in funcs), 'multi_ops can only apply functions to the first argument'
    assert len(funcs), 'multi_ops needs at least one function to apply to data_stream'

    for i in data_stream:
        if len(funcs) > 1:
            yield tuple(func(i) for func in funcs)
        elif len(funcs) == 1:
            yield funcs[0](i)

del noglobals

if __name__ == '__main__':
    # example usage below
    def test_function(arg):
        return arg+arg

    gen = (i for i in range(10))

    gen = (i*2 for i in gen)

    gen = multi_ops(
        gen,
        int,
        float,
        str,
        bool,
        lambda i: i**2,
        test_function
    )

    for i in gen:
        print(i)
