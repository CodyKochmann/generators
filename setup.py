from distutils.core import setup
import sys

setup(
  name = 'generators',
  packages = ['generators'], # this must be the same as the name above
  install_requires = (["strict_functions", "future"] if sys.version_info < (3,0) else ["strict_functions"]),
  version = '2018.1.24',
  description = 'collection of helpful generators that should have been in itertools',
  author = 'Cody Kochmann',
  author_email = 'kochmanncody@gmail.com',
  url = 'https://github.com/CodyKochmann/generators',
  download_url = 'https://github.com/CodyKochmann/generators/tarball/2018.1.1',
  keywords = ['generators', 'iter', 'itertools', 'combinations', 'chain', 'iterate', 'gen'],
  classifiers = [],
)
