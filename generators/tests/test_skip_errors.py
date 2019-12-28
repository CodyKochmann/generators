#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Cody Kochmann
# @Date:   2017-09-09
# @Last Modified 2017-10-17

import unittest
from generators import G

def _double_only_evens(i):
    if i%2==1:
        raise ValueError()
    return i*2

class Test_skip_errors(unittest.TestCase):
    ''' this runs tests to verify behavior of generators.chunks '''
    def test_skip_errors_basic(self):
        ''' test the basic usage of skip_errors '''
        self.assertRaises(
             ValueError,
             lambda: G(range(5)).map(_double_only_evens).to(list)
        )
        self.assertEqual(
            G(range(5)).map(_double_only_evens).skip_errors().to(list),
            [0, 4, 8]
        )
    def test_skip_errors_with_log_true(self):
        ''' test skip_errors with log specifically enabled '''
        self.assertEqual(
            G(range(5)).map(_double_only_evens).skip_errors(log=True).to(list),
            [0, 4, 8]
        )
    def test_skip_errors_with_log_false(self):
        ''' test skip_errors with log specifically enabled '''
        self.assertEqual(
            G(range(5)).map(_double_only_evens).skip_errors(log=False).to(list),
            [0, 4, 8]
        )

if __name__ == '__main__':
    unittest.main(verbosity=2)
