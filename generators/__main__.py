# -*- coding: utf-8 -*-
# @Author: Cody Kochmann

import sys
import argparse

parser = argparse.ArgumentParser(prog='__main__.py')

parser.add_argument(
    '--test',
    help="run tests to see if generators works correctly on you system",
    action='store_true'
)
#parser.add_argument(
#    '--benchmark',
#    help="test how fast generators can run on your system",
#    action='store_true'
#)

if '__main__.py' in sys.argv[-1] or 'help' in sys.argv:
    parsed = parser.parse_args(['-h'])

args, unknown = parser.parse_known_args()

if args.test:
    import os, sys, generators
    prev = os.getcwd()
    try:
        os.chdir(min(generators.__path__, key=len))
        os.system('{} -m unittest --verbose'.format(sys.executable))
    finally:
        os.chdir(prev)
