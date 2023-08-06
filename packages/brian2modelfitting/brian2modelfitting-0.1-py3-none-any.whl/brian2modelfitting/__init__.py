'''
Tools for use with the Brian 2 simulator.
'''
import os

from .modelfitting import *
from .tests import run as test

try:
    # Use version written out by setuptools
    from .version import version
    __version__ = version
except ImportError:
    # Apparently we are running directly from a git clone, let
    # setuptools_scm fetch the version from git
    from setuptools_scm import get_version
    __version__ = get_version(relative_to=os.path.dirname(__file__))
    version = __version__
