#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' these are tools that make writing and debugging inline generators easier '''

import sys
import os.path

sys.path.append(os.path.dirname(__file__))

del sys
del os

from time_pipeline import time_pipeline
from cpu_time import cpu_time
