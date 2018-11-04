import unittest
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

class Test_apply_to_last(unittest.TestCase):
    def test_apply_to_last_basic(self):
        self.assertEqual(
            list(apply_to_last(range(10), lambda i:i*2)),
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 18],
            'invalid output of basic usage'
        )
    def test_apply_to_last_input_validation(self):
        with self.assertRaises(AssertionError):
            list(apply_to_last([1, 2, 3], [1, 2, 3]))
        with self.assertRaises(AssertionError):
            list(apply_to_last(3, lambda i:None))

if __name__ == '__main__':
    unittest.main(verbosity=2)
