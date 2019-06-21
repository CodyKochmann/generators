import unittest
from strict_functions import strict_globals
from iterable import iterable

@strict_globals(iterable=iterable)
def apply_to_last(stream, fn):
    ''' applies a given function to the last item in a generator/stream '''
    assert iterable(stream), 'apply_to_last needs stream to be iterable'
    assert callable(fn), 'apply_to_last needs fn to be callable'

    stream = iter(stream)
    for previous in stream:
        for current in stream:
            yield previous
            previous = current
        yield fn(previous)
        break

del iterable
del strict_globals
