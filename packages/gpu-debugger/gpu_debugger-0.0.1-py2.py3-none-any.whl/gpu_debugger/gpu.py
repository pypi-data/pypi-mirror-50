# -*- coding: utf-8 -*-
"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
[options.entry_points] section in setup.cfg:

    console_scripts =
         fibonacci = gpu_debugger.skeleton:run

Then run `python setup.py install` which will install the command `fibonacci`
inside your current environment.
Besides console scripts, the header (i.e. until _logger...) of this file can
also be used as template for Python modules.

Note: This skeleton file can be safely removed if not needed!
"""

import argparse
import sys
import logging
from enum import Enum
from pynvml import *
import unittest

__author__ = "kula"
__copyright__ = "kula"
__license__ = "mit"

_logger = logging.getLogger(__name__)

class DEBUG_LEVEL(Enum):
    INFO = 0  
    TRACE = 1 
    DEBUG = 2 
    WARN = 3 
    ERROR = 4 
    FATAL = 5 



def print_memory(level = DEBUG_LEVEL.INFO, index=0):
    nvmlInit()
    handle = nvmlDeviceGetHandleByIndex(index)
    info = nvmlDeviceGetMemoryInfo(handle)
    print("gpu:{}:{}MB memory used".format(level.name, info.used/(1024*1024)))


class TestCase(unittest.TestCase):

    def test_print_memory(self):
        print_memory()

if __name__ == '__main__':
    unittest.main()