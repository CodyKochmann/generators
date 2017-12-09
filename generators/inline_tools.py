#!/usr/bin/env python

from __future__ import print_function
_print = print
del print_function

from inspect import getsource
from strict_functions import strict_globals, noglobals

__all__ = 'asserts', 'print', 'attempt'


@strict_globals(getsource=getsource)
def asserts(input_value, rule, message=''):
    """ this function allows you to write asserts in generators since there are
        moments where you actually want the program to halt when certain values
        are seen.
    """
    assert callable(rule) or type(rule)==bool, 'asserts needs rule to be a callable function or a test boolean'
    assert isinstance(message, str), 'asserts needs message to be a string'
    # if the message is empty and rule is callable, fill message with rule's source code
    if len(message)==0 and callable(rule):
        try:
            s = getsource(rule).splitlines()[0].strip()
        except:
            s = repr(rule).strip()
        message = 'illegal input of {} breaks - {}'.format(input_value, s)
    if callable(rule):
        # if rule is a function, run the function and assign it to rule
        rule = rule(input_value)
    # now, assert the rule and return the input value
    assert rule, message
    return input_value

del getsource

@strict_globals(_print=_print)
def print(*a):
    """ print just one that returns what you give it instead of None """
    try:
        _print(*a)
        return a[0] if len(a) == 1 else a
    except:
        _print(*a)

del _print

@noglobals
def attempt(fn, default_output=None):
    ''' attempt running a function in a try block without raising exceptions '''
    assert callable(fn), 'generators.inline_tools.attempt needs fn to be a callable function'
    try:
        return fn()
    except:
        return default_output

del strict_globals, noglobals

if __name__ == '__main__':
    print(print(attempt(lambda:1/0)))
    print(print(attempt(lambda:1/2)))
    print(print(attempt(lambda:asserts(1, lambda i:1/i))))
    print(asserts(0, lambda i:1>i))
    asserts(2, lambda i:1>i)
