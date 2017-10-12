# -*- coding: utf-8 -*-
# @Author: Cody Kochmann
# @Date:   2017-10-12 12:11:03
# @Last Modified 2017-10-12
# @Last Modified time: 2017-10-12 12:12:37

""" this behaves as a shortcut for the rps function in performance_tools """

import sys
import os.path

sys.path.append(os.path.dirname(__file__))

del sys
del os

from performance_tools import runs_per_second as rps
