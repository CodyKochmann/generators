# -*- coding: utf-8 -*-
# @Author: Cody Kochmann

from sys import argv
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

if '__main__.py' in argv[-1] or 'help' in argv:
    parsed = parser.parse_args(['-h'])

args, unknown = parser.parse_known_args()

if args.test:
    print('running unittests for generators')
    from generators.__test__ import main
    main(verbosity=2)
