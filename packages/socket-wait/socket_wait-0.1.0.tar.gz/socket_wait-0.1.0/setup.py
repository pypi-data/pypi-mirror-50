__author__ = 'tcaruso'

# !/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import fnmatch
import os
import sys
import warnings
from shutil import rmtree
from setuptools import find_packages, setup, Command
from collections import namedtuple

try:
    from pip._internal.req import parse_requirements
except ImportError:
    from pip.req import parse_requirements
except Exception:
    from pip import __version__ as __pip_version__

    msg = """Sorry, could not install due to a pip import error. Please open an issue on the repo 
    with this message and the error so it can be addressed.

    pip version: {}
    python version: {}

    """.format(__pip_version__, '.'.join(sys.version_info))
    raise EnvironmentError(msg)

here = os.path.abspath(os.path.dirname(__file__))

# ------------------------------------------------

# Package meta-data.
# PACKAGE_NAME is the name of the package directory and the import path. If you use my_package then when installed, you
# will import the package like `import my_package`.
PACKAGE_NAME = 'socket_wait'
DESCRIPTION = 'Listen on a port until a connection is received.'
URL = 'https://github.com/tomplex/socket_wait'
EMAIL = 'carusot42@gmail.com'
AUTHOR = 'Tom Caruso'
# The minimum Python version required
REQUIRES_PYTHON = (2, 7, 0)
# PYPI_NAME is the name of the package on pypi. We'll default to pbvt_{PACKAGE_NAME} so we avoid name collisions
# with PyPI. You'll use this name to install the package.
PYPI_NAME = '{}'.format(PACKAGE_NAME)
# Specify the name of the requirements file we should use. If there is none, then just leave it as is. We'll detect

# ------------------------------------------------
# Check Python version we're installing against. Bail if it's not correct. This will blow up both when we build the
# package and when someone tries to install it.

if sys.version_info < REQUIRES_PYTHON:
    # Raise if we're trying to install on an unsupported Python version
    raise Exception("Package {} requires python >= {}.".format(PYPI_NAME, '.'.join(map(str, REQUIRES_PYTHON))))

REQUIRES_PYTHON = '>=' + '.'.join(map(str, REQUIRES_PYTHON))


# ------------------------------------------------
# Requirements gathering.


about = {}
from socket_wait import __version__

about['__version__'] = __version__


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status("Installing required build packages...")
        os.system('{0} -m pip install wheel twine'.format(sys.executable))

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to pypi via Twine…')
        os.system('{0} -m twine upload dist/* '.format(sys.executable))

        sys.exit()


setup(
    name=PYPI_NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    py_modules=['socket_wait'],
    include_package_data=False,
    # If your package has a CLI component, specify it in entry_points.
    # for example, if you want it to be called like "mycli" from the command line, and the command line entry
    # point lives in the somepackage/cli.py file, in the function main, you'd construct it like this:
    entry_points={
        'console_scripts': ['socket_wait=socket_wait:cli'],
    },

    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    # setup.py publish support.
    cmdclass={
        'upload': UploadCommand,
    },
)
