#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Cody Kochmann
# @Date:   2017-09-09
# @Last Modified 2017-10-17

import unittest

try:
    from itertools import zip_longest
except ImportError:
    from itertools import izip_longest as zip_longest, imap as map
else:
    map = map

from strict_functions import strict_globals
from chunk_on import chunk_on
from apply_to_last import apply_to_last
from iterable import iterable

@strict_globals(zip_longest=zip_longest, apply_to_last=apply_to_last, chunk_on=chunk_on, iterable=iterable, map=map)
def chunks(stream, chunk_size, output_type=tuple):
    ''' returns chunks of a stream '''
    assert iterable(stream), 'chunks needs stream to be iterable'
    assert (isinstance(chunk_size, int) and chunk_size > 0) or callable(chunk_size), 'chunks needs chunk_size to be a positive int or callable'
    assert callable(output_type), 'chunks needs output_type to be callable'
    if callable(chunk_size):
        ''' chunk_size is acting as a separator function '''
        for chunk in chunk_on(stream, chunk_size, output_type):
            yield chunk
    else:
        it = iter(stream)
        marker = object()
        iters = [it] * chunk_size
        pipeline = apply_to_last(
           zip_longest(*iters, fillvalue=marker),
           lambda last_chunk: tuple(i for i in last_chunk if i is not marker)
        )
        if output_type is not tuple:
            pipeline = map(output_type, pipeline)
        for chunk in pipeline:
            yield chunk

del zip_longest
del apply_to_last
del chunk_on
del map
del strict_globals

#==============================================================
# Test code below:
#==============================================================

class Test_chunks(unittest.TestCase):
    ''' this runs tests to verify behavior of generators.chunks '''
    def test_chunks_basic(self):
        ''' test the basic usage of chunks '''
        l = list(range(30))

        self.assertEqual(
            list(chunks(l, 2)),
            [(0, 1), (2, 3), (4, 5), (6, 7), (8, 9), (10, 11), (12, 13), (14, 15), (16, 17), (18, 19), (20, 21), (22, 23), (24, 25), (26, 27), (28, 29)]
        )
        self.assertEqual(
            list(chunks(l, 15)),
            [(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14), (15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29)]
        )
        self.assertEqual(
            list(chunks(l, 20)),
            [(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19), (20, 21, 22, 23, 24, 25, 26, 27, 28, 29)]
        )
        self.assertEqual(
            list(chunks(l, 2, set)),
            [{0, 1}, {2, 3}, {4, 5}, {6, 7}, {8, 9}, {10, 11}, {12, 13}, {14, 15}, {16, 17}, {18, 19}, {20, 21}, {22, 23}, {24, 25}, {26, 27}, {28, 29}]
        )
        self.assertEqual(
            list(chunks(l, 15, set)),
            [{0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14}, {15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29}]
        )
        self.assertEqual(
            list(chunks(l, 20, set)),
            [{0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19}, {20, 21, 22, 23, 24, 25, 26, 27, 28, 29}]
        )
        self.assertEqual(
            list(chunks(l, lambda i:i==15)),
            [(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14), (15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29)]
        )
        self.assertEqual(
            list(chunks(l, lambda i:i%5==0)),
            [(0, 1, 2, 3, 4), (5, 6, 7, 8, 9), (10, 11, 12, 13, 14), (15, 16, 17, 18, 19), (20, 21, 22, 23, 24), (25, 26, 27, 28, 29)]
        )
        self.assertEqual(
            list(chunks(l, lambda i:str(i).startswith('1'))),
            [(0,), (1, 2, 3, 4, 5, 6, 7, 8, 9), (10,), (11,), (12,), (13,), (14,), (15,), (16,), (17,), (18,), (19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29)]
        )

    def test_chunks_ranged(self, test_range=10, chunk_size=2):
        pipe = chunks(range(test_range), chunk_size)
        for first_digit in range(0, test_range, chunk_size):
            expected_chunk = tuple((i for i in range(first_digit, first_digit+chunk_size) if i < test_range))
            chunk = next(pipe)
            self.assertTrue(isinstance(chunk, tuple), msg='incorrect chunk type')
            self.assertEqual(len(expected_chunk), len(chunk), msg='incorrect chunk size')
            self.assertEqual(expected_chunk, chunk, msg='invalid chunk')

    def test_chunks_multi_ranged(self):
        for chunk_size in range(1, 30):
            self.test_chunks_ranged(test_range=1000, chunk_size=chunk_size)

    def test_chunks_output_type(self):
        for t in (tuple, list, str):
            self.assertEqual(type(next(chunks(range(10), 2, output_type=t))), t, 'invalid custom output type')

    def test_chunks_input_validation(self):
        with self.assertRaises(AssertionError):
            list(chunks(1, 2))
        with self.assertRaises(AssertionError):
            list(chunks(range(10), 'hi'))
        with self.assertRaises(AssertionError):
            list(chunks(range(10), 2, 'fishsticks'))


if __name__ == '__main__':
    unittest.main(verbosity=2)