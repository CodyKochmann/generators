import collections
import os
import sys
import unittest

sys.path.append(os.path.dirname(__file__))

from chunks import Test_chunks
from apply_to_last import Test_apply_to_last

if __name__ == '__main__':
    unittest.main(verbosity=2)
