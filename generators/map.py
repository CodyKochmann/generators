
"""
what does map do

- run first argument (the function) against the input iterables
- if multiple iterables are defined, multiple inputs are required for the function

what does our map do

- run multi-ops if multiple functions are given
- run window or chunks if multiple args in function

"""

from multi_ops import multi_ops
from window import window
from strict_functions import noglobals, strict_globals

@noglobals
def function_arg_count(fn):
    """ returns how many arguments a funciton has """
    assert callable(fn), 'function_arg_count needed a callable function, not {0}'.format(repr(fn))
    if hasattr(fn, '__code__') and hasattr(fn.__code__, 'co_argcount'):
        return fn.__code__.co_argcount
    else:
        return 1 # not universal, but for now, enough... :/


@strict_globals(function_arg_count=function_arg_count, multi_ops=multi_ops, window=window)
def map(*args):
    """ this map works just like the builtin.map, except, this one you can also:
        - give it multiple functions to map over an iterable
        - give it a single function with multiple arguments to run a window
          based map operation over an iterable
    """

    functions_to_apply = [i for i in args if callable(i)]
    iterables_to_run = [i for i in args if not callable(i)]
    #print('functions_to_apply:',functions_to_apply)
    #print('iterables_to_run:',iterables_to_run)

    assert len(functions_to_apply)>0, 'at least one function needs to be given to map'
    assert len(iterables_to_run)>0, 'no iterables were given to map'

    # check for native map usage
    if len(functions_to_apply) == 1 and len(iterables_to_run) >= 1 and function_arg_count(*functions_to_apply)==1:
        if hasattr(iter([]), '__next__'): # if python 3
            return __builtins__.map(functions_to_apply[0], *iterables_to_run)
        else:
            return iter(__builtins__.map(functions_to_apply[0], *iterables_to_run))
    # ---------------------------- new logic below ----------------------------
    # logic for a single function
    elif len(functions_to_apply) == 1:
        fn = functions_to_apply[0]
        # if there is a single iterable, chop it up
        if len(iterables_to_run) == 1:
            return (fn(*i) for i in window(iterables_to_run[0], function_arg_count(functions_to_apply[0])))
    # logic for more than 1 function
    elif len(functions_to_apply) > 1 and len(iterables_to_run) == 1:
        return multi_ops(*(iterables_to_run + functions_to_apply))
    else:
        raise ValueError('invalid usage of map()')


del function_arg_count, window, multi_ops, noglobals, strict_globals


if __name__ == '__main__':

    # example usage

    l = list(range(10))

    def show(generator):
        ''' prints a generator '''
        print('-'*30)
        print(list(generator))
        print('-'*30)

    show(l)

    show(map(int, bool, float, l))

    show(map(bool, l))

    show(map(lambda a,b:a+b, l))

