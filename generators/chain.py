# -*- coding: utf-8 -*-
# @Author: Cody Kochmann
# @Date:   2017-09-09 14:58:43
# @Last Modified by:   Cody Kochmann
# @Last Modified time: 2017-12-09 10:27:36

from functools import partial
from strict_functions import strict_globals

@strict_globals(partial=partial)
def chain(*args):
    """itertools.chain, just better"""
    has_iter = partial(hasattr, name='__iter__')
    # check if a single iterable is being passed for
    # the case that it's a generator of generators
    if len(args) == 1 and hasattr(args[0], '__iter__'):
        args = args[0]

    for arg in args:
        # if the arg is iterable
        if hasattr(arg, '__iter__'):
            # iterate through it
            for i in arg:
                yield i
        # otherwise
        else:
            # yield the whole argument
            yield arg

del partial
del strict_globals

if __name__ == '__main__':
    import itertools as itr

    def show(generator):
        ''' prints a generator '''
        print('-'*30)
        print(tuple(generator))
        print('-'*30)

    show(chain())

    # this is a generator of generators
    g = (iter(range(10)) for i in range(10))
    show(chain(g))

    # doing this in itertools would do this
    g = (iter(range(10)) for i in range(10))
    show(itr.chain(g))

