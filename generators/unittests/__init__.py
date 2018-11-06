''' this makes the unittests importable '''

import sys
from os.path import abspath, dirname
from unittest import main

# this adds everything in the directory above to the importable path of this directory
__file_path__ = abspath(__file__)
__file_dir__ = dirname(__file_path__)
sys.path.append(__file_dir__)

from test_apply_to_last import *
from test_chunks import *

sys.path.remove(__file_dir__)
