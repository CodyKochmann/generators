#!/usr/bin/env python

from __future__ import print_function
del print_function

from inspect import getsource

__all__ = 'asserts', 'print'

_print = print

def asserts(input_args, rule, message=''):
    """ this function allows you to write asserts in generators since there are
        moments where you actually want the program to halt when certain values
        are seen.
    """
    assert callable(rule), 'asserts needs rule to be a callable function'
    assert type(message).__name__ in ('str', 'unicode'), 'asserts needs message to be a string'
    if message == '':
        try:
            s = getsource(rule).splitlines()[0].strip()
        except:
            s = repr(rule).strip()
        message = 'illegal input of {} breaks - {}'.format(input_args, s)
    assert rule(input_args), message
    return input_args

def print(*a):
    """ print just one that returns what you give it instead of None """
    try:
        _print(*a)
        return a[0] if len(a) == 1 else a
    except:
        _print(*a)
