from distutils.core import setup

setup(
  name = 'generators',
  packages = ['generators'], # this must be the same as the name above
  install_requires = ["strict_functions", "future"],
  version = '2017.12.9',
  description = 'collection of helpful generators that should have been in itertools',
  author = 'Cody Kochmann',
  author_email = 'kochmanncody@gmail.com',
  url = 'https://github.com/CodyKochmann/generators',
  download_url = 'https://github.com/CodyKochmann/generators/tarball/2017.12.9',
  keywords = ['generators', 'iter', 'itertools', 'combinations', 'chain', 'iterate', 'gen'],
  classifiers = [],
)
