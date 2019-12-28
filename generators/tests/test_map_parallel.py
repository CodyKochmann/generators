#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Cody Kochmann
# @Date:   2017-09-09
# @Last Modified 2017-10-17

import unittest
from generators import G

class Test_map_parallel(unittest.TestCase):
    ''' this runs tests to verify behavior of generators.map_parallel '''
    def test_map_parallel_basic(self):
        ''' test the basic usage of map_parallel '''
        self.assertEqual(
            G(range(5)).map_parallel(float, 2).to(list),
            [0.0, 1.0, 2.0, 3.0, 4.0]
        )
        self.assertEqual(
            G(range(5)).map_parallel(float, 3).to(list),
            [0.0, 1.0, 2.0, 3.0, 4.0]
        )
        self.assertEqual(
            G(range(5)).map_parallel(float, 4).to(list),
            [0.0, 1.0, 2.0, 3.0, 4.0]
        )
        self.assertEqual(
            G(range(5)).map_parallel(float, 5).to(list),
            [0.0, 1.0, 2.0, 3.0, 4.0]
        )
        self.assertEqual(
            G(range(5)).map_parallel(float, 6).to(list),
            [0.0, 1.0, 2.0, 3.0, 4.0]
        )
        self.assertEqual(
            G(range(5)).map_parallel(float, 7).to(list),
            [0.0, 1.0, 2.0, 3.0, 4.0]
        )
        self.assertEqual(
            G(range(5)).map_parallel(float, 8).to(list),
            [0.0, 1.0, 2.0, 3.0, 4.0]
        )

if __name__ == '__main__':
    unittest.main(verbosity=2)
