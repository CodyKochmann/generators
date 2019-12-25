from __future__ import print_function
from distutils.core import setup
import sys, os, setuptools

version = '2019.12.25'
name = 'generators'
packages = setuptools.find_packages()

assert name in packages, [name, packages]  # if package name doesnt show up, something is wrong

def using_ios_stash():
    ''' returns true if sys path hints the install is running on ios '''
    print('detected install path:')
    print(os.path.dirname(__file__))
    module_names = set(sys.modules.keys())
    return 'stash' in module_names or 'stash.system' in module_names

def requires():
    ''' generates a list of requirements for generators '''
    yield 'strict_functions'
    # only require future if using py2 and not using stash in ios
    if sys.version_info < (3,0):
        if not using_ios_stash():
            yield 'future'


setup(
  name = name,
  version = version,
  packages = packages,
  install_requires = list(requires()),
  zip_safe=True,
  description = 'a high performance pipeline processor written in python',
  author = 'Cody Kochmann',
  author_email = 'kochmanncody@gmail.com',
  url = 'https://github.com/CodyKochmann/generators',
  download_url = 'https://github.com/CodyKochmann/generators/tarball/{}'.format(version),
  keywords = ['generators', 'iter', 'itertools', 'combinations', 'pipe', 'pipeline', 'performance', 'fast', 'chain', 'iterate', 'gen', 'Generator'],
  classifiers = []
)
