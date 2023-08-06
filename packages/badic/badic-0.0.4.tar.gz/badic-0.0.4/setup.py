# setup.py : file that explains what need to be installed
#
# pip: python package manager
#   pip install xxx
#   pip install xxx
#
# sage -pip install --user --upgrade .
#
# sage -pip install --user --editable . # to prevent sage to copy sources

from __future__ import print_function, absolute_import

import sys
from distutils.core import setup
from setuptools.extension import Extension
#from warnings import warn
import warnings
from setuptools.command.test import test as TestCommand # for tests
from distutils.command.build_ext import build_ext as _build_ext

import numpy as np

def readfile(filename):
    with open(filename, "r") as f:
        return f.read()

class build_ext(_build_ext):
    def finalize_options(self):
        import subprocess
        from Cython.Build import cythonize
        import json

        # run the configure script
        subprocess.check_call(["make", "configure"])
        try:
            subprocess.check_call(["sh", "./configure"])
        except subprocess.CalledProcessError:
            subprocess.check_call(["cat", "config.log"])

        # configure created config.json that we can no read
        config = json.load(open("./config.json"))
        HAVE_SDL2 = config['HAVE_SDL2']

        for mod in self.distribution.ext_modules:
            mod.define_macros.append(('SDL_PRESENT', int(HAVE_SDL2)))
            mod.define_macros.append(('SDL_IMAGE_PRESENT', int(HAVE_SDL2)))
            if HAVE_SDL2:
                mod.libraries.append('SDL2')

        self.distribution.ext_modules[:] = cythonize(
            self.distribution.ext_modules, include_path=sys.path)
        _build_ext.finalize_options(self)

# For the tests
class SageTest(TestCommand):
    def run_tests(self):
        errno = os.system("sage -t --force-lib badic")
        if errno != 0:
            sys.exit(1)


extensions = [
              Extension("badic.cautomata",
                        sources=['badic/cautomata.pyx', 'badic/automataC.c']),
              
              Extension("badic.beta_adic",
                        sources=['badic/beta_adic.pyx', 'badic/complex.c', 'badic/draw.c', 'badic/relations.c', 'badic/automataC.c'],
                        include_dirs=[np.get_include()])
              ]

setup(
    name='badic',
    packages=['badic/'],
    description='Beta-adics and automata tools',
    long_description = readfile("README"), # get the long description from the README
    url='https://gitlab.com/mercatp/badic',
    author='Paul Mercat, Dominique Benielli',
    author_email='paul.mercat@univ-amu.fr', # choose a main contact email
    license='GPLv3.0', # This should be consistent with the LICENCE file
    classifiers=[
      # How mature is this project? Common values are
      #   3 - Alpha
      #   4 - Beta
      #   5 - Production/Stable
      'Development Status :: 4 - Beta',
      'Intended Audience :: Science/Research',
      'Topic :: Software Development :: Build Tools',
      'Topic :: Scientific/Engineering :: Mathematics',
      'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
      'Programming Language :: Python :: 2.7',
      'Programming Language :: Python :: 3',
      'Programming Language :: Cython',
      'Programming Language :: C',
    ], # classifiers list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords = "SageMath beta-adic automata",
    cmdclass = {'build_ext': build_ext, 'test': SageTest}, # adding a special setup command for tests
    version='0.0.4',
    ext_modules=extensions
)
