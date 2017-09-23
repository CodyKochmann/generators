#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' inline asserts for python one liner madness '''

from inspect import getsource

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


if __name__ == '__main__':
    # example code below

    is_even = lambda i: not i%2
    is_positive = lambda i: i > 0

    l = list(range(20))

    g = (i*3 for i in l)
    g = (asserts(i, is_positive) for i in g)
    g = (asserts(i, is_even) for i in g)

    list(g)

