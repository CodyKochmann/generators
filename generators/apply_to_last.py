from strict_functions import strict_globals
from iterable import iterable

@strict_globals(iterable=iterable)
def apply_to_last(stream, fn):
    ''' applies a given function to the last item in a generator/stream '''
    assert iterable(stream), 'apply_to_last needs stream to be iterable'
    assert callable(fn), 'apply_to_last needs fn to be callable'

    stream = iter(stream)
    previous = next(stream)
    for current in stream:
        yield previous
        previous = current
    yield fn(previous)

del iterable
del strict_globals

if __name__ == '__main__':
    print(list(apply_to_last(range(10), lambda i:i*2)))
