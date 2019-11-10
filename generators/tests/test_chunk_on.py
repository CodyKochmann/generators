#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Cody Kochmann
# @Date:   2017-09-09
# @Last Modified 2017-10-17

from functools import partial
import unittest
from generators import chunk_on

class Test_chunk_on(unittest.TestCase):
    ''' this runs tests to verify behavior of generators.chunks '''
    def test_chunk_on_basic_1(self):
        ''' test the basic usage of chunks '''
        l = list(range(30))
        self.assertEqual(
            list(chunk_on(l, lambda i:i%3==0)),
            [(0, 1, 2), (3, 4, 5), (6, 7, 8), (9, 10, 11), (12, 13, 14), (15, 16, 17), (18, 19, 20), (21, 22, 23), (24, 25, 26), (27, 28, 29)]
        )
    def test_chunk_on_basic_2(self):
        ''' test the basic usage of chunks '''
        l = list(range(30))
        self.assertEqual(
            list(chunk_on(l, lambda i:i==15)),
            [(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14), (15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29)]
        )
    def test_chunk_on_basic_3(self):
        ''' test the basic usage of chunks '''
        l = list(range(30))
        self.assertEqual(
            list(chunk_on(l, lambda i:i%5==0)),
            [(0, 1, 2, 3, 4), (5, 6, 7, 8, 9), (10, 11, 12, 13, 14), (15, 16, 17, 18, 19), (20, 21, 22, 23, 24), (25, 26, 27, 28, 29)]
        )
    def test_chunk_on_basic_4(self):
        ''' test the basic usage of chunks '''
        l = list(range(30))
        self.assertEqual(
            list(chunk_on(l, lambda i:str(i).startswith('1'))),
            [(0,), (1, 2, 3, 4, 5, 6, 7, 8, 9), (10,), (11,), (12,), (13,), (14,), (15,), (16,), (17,), (18,), (19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29)]
        )

    def validate_chunk_on_output_type(self, t):
        assert type(t) == type
        self.assertEqual(type(next(chunk_on(range(10), (lambda i:i%2==1), output_type=t))), t, 'invalid custom output type')

    def test_chunk_on_tuple_output(self):
        self.validate_chunk_on_output_type(tuple)
    def test_chunk_on_list_output(self):
        self.validate_chunk_on_output_type(list)
    def test_chunk_on_str_output(self):
        self.validate_chunk_on_output_type(str)
    def test_chunk_on_bool_output(self):
        self.validate_chunk_on_output_type(bool)


    def test_chunk_on_input_validation(self):
        #with self.assertRaises(AssertionError):
        #    list(chunk_on(1, 2))
        #with self.assertRaises(AssertionError):
        #    list(chunk_on(range(10), 'hi'))
        #with self.assertRaises(AssertionError):
        #    list(chunk_on(range(10), 2))
        pass

if __name__ == '__main__':
    unittest.main(verbosity=2)
