#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Cody Kochmann
# @Date:   2017-09-09
# @Last Modified 2017-10-17

import unittest
from generators import chunks, G

class Test_chunks(unittest.TestCase):
    ''' this runs tests to verify behavior of generators.chunks '''
    def test_chunks_basic_1(self):
        ''' test the basic usage of chunks '''
        l = list(range(30))

        self.assertEqual(
            list(chunks(l, 2)),
            [
                (0, 1),
                (2, 3),
                (4, 5),
                (6, 7),
                (8, 9),
                (10, 11),
                (12, 13),
                (14, 15),
                (16, 17),
                (18, 19),
                (20, 21),
                (22, 23),
                (24, 25),
                (26, 27),
                (28, 29)
            ]
        )

    def test_chunks_basic_2(self):
        ''' test the basic usage of chunks '''
        l = list(range(30))

        self.assertEqual(
            list(chunks(l, 15)),
            [
                ( 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14),
                (15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29)
            ]
        )

    def test_chunks_basic_3(self):
        ''' test the basic usage of chunks '''
        l = list(range(30))

        self.assertEqual(
            list(chunks(l, 20)),
            [
                ( 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19),
                (20, 21, 22, 23, 24, 25, 26, 27, 28, 29)
            ]
        )

    def test_chunks_basic_4(self):
        ''' test the basic usage of chunks '''
        l = list(range(30))

        self.assertEqual(
            list(chunks(l, 2, output_type=list)),
            [
                [ 0,  1],
                [ 2,  3],
                [ 4,  5],
                [ 6,  7],
                [ 8,  9],
                [10, 11],
                [12, 13],
                [14, 15],
                [16, 17],
                [18, 19],
                [20, 21],
                [22, 23],
                [24, 25],
                [26, 27],
                [28, 29]
            ]
        )

    def test_chunks_basic_5(self):
        ''' test the basic usage of chunks '''
        l = list(range(30))

        self.assertEqual(
            list(chunks(l, 15, output_type=list)),
            [
                [ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14],
                [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
            ]
        )

    def test_chunks_basic_6(self):
        ''' test the basic usage of chunks '''
        l = list(range(30))

        self.assertEqual(
            list(chunks(l, 20, output_type=list)),
            [
                [ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
                [20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
            ]
        )

    def test_chunks_basic_7(self):
        ''' test the basic usage of chunks '''
        l = list(range(30))

        self.assertEqual(
            list(chunks(l, lambda i:i==15)),
            [
                ( 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14),
                (15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29)
            ]
        )

    def test_chunks_basic_8(self):
        ''' test the basic usage of chunks '''
        l = list(range(30))

        self.assertEqual(
            list(chunks(l, lambda i:i%5==0)),
            [
                ( 0,  1,  2,  3,  4),
                ( 5,  6,  7,  8,  9),
                (10, 11, 12, 13, 14),
                (15, 16, 17, 18, 19),
                (20, 21, 22, 23, 24),
                (25, 26, 27, 28, 29)
            ]
        )

    def test_chunks_basic_9(self):
        ''' test the basic usage of chunks '''
        l = list(range(30))

        self.assertEqual(
            list(chunks(l, lambda i:str(i).startswith('1'))),
            [
                ( 0,),
                ( 1,  2,  3,  4,  5,  6,  7,  8,  9),
                (10,),
                (11,),
                (12,),
                (13,),
                (14,),
                (15,),
                (16,),
                (17,),
                (18,),
                (19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29)
            ]
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

    def test_chunks_2_dimensional(self):
        self.assertEqual(
            list(chunks(range(18), 3, 3)),
            [
                (
                    (0, 1, 2),
                    (3, 4, 5),
                    (6, 7, 8)
                ),
                (
                    ( 9, 10, 11),
                    (12, 13, 14),
                    (15, 16, 17)
                )
            ]
        )

    def test_chunks_3_dimensional(self):
        self.assertEqual(
            list(chunks(range(16), 2, 2, 2)),
            [
                (
                    (
                        (0, 1),
                        (2, 3)
                    ),
                    (
                        (4, 5),
                        (6, 7)
                    )
                ),
                (
                    (
                        ( 8,  9),
                        (10, 11)
                    ),
                    (
                        (12, 13),
                        (14, 15)
                    )
                ),
            ]
        )

    def test_chunks_2_dimensional_g_usage(self):
        self.assertEqual(
            G(range(18)).chunk(3, 3).to(list),
            [
                (
                    (0, 1, 2),
                    (3, 4, 5),
                    (6, 7, 8)
                ),
                (
                    ( 9, 10, 11),
                    (12, 13, 14),
                    (15, 16, 17)
                )
            ]
        )

    def test_chunks_3_dimensional_g_usage(self):
        self.assertEqual(
            G(range(16)).chunk(2, 2, 2).to(list),
            [
                (
                    (
                        (0, 1),
                        (2, 3)
                    ),
                    (
                        (4, 5),
                        (6, 7)
                    )
                ),
                (
                    (
                        ( 8,  9),
                        (10, 11)
                    ),
                    (
                        (12, 13),
                        (14, 15)
                    )
                ),
            ]
        )

if __name__ == '__main__':
    unittest.main(verbosity=2)
