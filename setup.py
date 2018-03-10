from distutils.core import setup
import sys

version = '2018.3.10'

def using_ios_stash():
    ''' returns true if sys path hints the install is running on ios '''
    return all(i in ' '.join(sys.argv).lower() for i in ['mobile', 'pythonista'])

def requires():
    ''' generates a list of requirements for generators '''
    yield 'strict_functions'
    if sys.version_info < (3,0):
        if not using_ios_stash():
            yield 'future'

setup(
  name = 'generators',
  packages = ['generators'], # this must be the same as the name above
  install_requires = list(requires()),
  version = version,
  description = 'collection of helpful generators that should have been in itertools',
  author = 'Cody Kochmann',
  author_email = 'kochmanncody@gmail.com',
  url = 'https://github.com/CodyKochmann/generators',
  download_url = 'https://github.com/CodyKochmann/generators/tarball/{}'.format(version),
  keywords = ['generators', 'iter', 'itertools', 'combinations', 'chain', 'iterate', 'gen', 'Generator'],
  classifiers = [],
)
