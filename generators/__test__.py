import collections
import os
import sys
import unittest
from unittest import main

sys.path.append(os.path.realpath(os.path.dirname(__file__)))

from unittests import *

if __name__ == '__main__':
    main(verbosity=2)
