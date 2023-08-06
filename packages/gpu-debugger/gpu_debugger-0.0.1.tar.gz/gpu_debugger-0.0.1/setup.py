# -*- coding: utf-8 -*-
"""
    Setup file for gpu_debugger.
    Use setup.cfg to configure your project.

    This file was generated with PyScaffold 3.2.1.
    PyScaffold helps you to put up the scaffold of your new Python project.
    Learn more under: https://pyscaffold.org/
"""
import sys

from pkg_resources import VersionConflict, require
from setuptools import setup

try:
    require('setuptools>=38.3')
except VersionConflict:
    print("Error: version of setuptools is too old (<38.3)!")
    sys.exit(1)

setup(
     name='gpu_debugger',
     version='0.0.1',
     author='kulasama',
     author_email='kulasama@foxmail.com',
     license='MIT',
     packages=['gpu_debugger'],
     install_requires=[
         'nvidia-ml-py3',
     ]
)