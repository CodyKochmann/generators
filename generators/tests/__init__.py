import os, sys
from importlib import import_module
from itertools import chain
from unittest import TestCase

# temporarily add this file's path to system path
sys.path.append(os.path.dirname(__file__))

# things defined here will tell python what to grab in `import *`
__all__ = []

# find the test python files in this directory
g = (i for i in os.listdir(os.path.dirname(__file__)) if i.startswith('test_') and i.endswith('.py'))
# import the modules
g = (import_module(i.strip('.py')) for i in g)
# grab the attributes
g = chain.from_iterable((getattr(i, ii) for ii in dir(i)) for i in g)
# filter out everything that isnt a subclass of TestCase
g = (i for i in g if isinstance(i, type) and issubclass(i, TestCase))
# sanitize the data
g = (i for i in g if i is not TestCase and hasattr(i, '__name__'))
# map the testcases to this file's namespace
for i in g:
	__all__.append(i.__name__)
	setattr(sys.modules[__name__], i.__name__, i)

# clean up system path
sys.path.remove(os.path.dirname(__file__))

# clean up namespace and free references that can be unloaded
del os
del sys
del import_module
del chain
del TestCase