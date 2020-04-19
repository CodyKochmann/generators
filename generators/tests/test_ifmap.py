#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Cody Kochmann
# @Date:   2017-09-09
# @Last Modified 2017-10-17

import unittest
from itertools import count
from generators import G, ifmap

class Test_ifmap(unittest.TestCase):
    ''' this runs tests to verify behavior of generators.ifmap '''
    def test_ifmap_basic_usage_1(self):
        ''' test the basic usage of ifmap '''
        self.assertEqual(
            list(ifmap(range(5), bool, str)),
            [0, "1", "2", "3", "4"]
        )

    def test_ifmap_basic_usage_2(self):
        ''' test the basic usage of ifmap '''
        self.assertEqual(
            list(ifmap(range(5), lambda i:i%2, double)),
            [0, "1", "2", "3", "4"]
        )

    def test_ifmap_basic_g_usage_1(self):
        ''' test the basic usage of ifmap with G invocation '''
        self.assertEqual(
            G(range(5)).ifmap(bool, str).to(list),
            [0, "1", "2", "3", "4"]
        )
        
    def test_ifmap_basic_g_usage_2(self):
        ''' test the basic usage of ifmap with G invocation '''
        self.assertEqual(
            G(range(5)).ifmap(lambda i:i%2, double).to(list),
            [0, "1", "2", "3", "4"]
        )

    def test_ifmap_benchmark_0(self):
        ''' test the basic usage of ifmap with G invocation '''
        self.assertGreater(
            G(count).ifmap(bool, str),
            1_000_000
        )

    def test_ifmap_benchmark_1(self):
        ''' test the basic usage of ifmap with G invocation '''
        self.assertGreater(
            G(count).ifmap(lambda i:i%2, double),
            1_000_000
        )

if __name__ == '__main__':
    unittest.main(verbosity=2)
