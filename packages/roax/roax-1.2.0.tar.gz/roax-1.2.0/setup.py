#!/usr/bin/env python3

import os
import re
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as _test

class test(_test):
    def finalize_options(self):
        _test.finalize_options(self)
        self.test_args.insert(0, 'discover')

def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()

install_requires = [
    "isodate >=0.6.0",
    "WebOb >=1.8.4",
    "wrapt >=1.10.11"
]

tests_require = [
    "redis >= 3.0.1",
]

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
]

setup(
    name = "roax",
    version = "1.2.0",
    description = "Lightweight framework for building resource-oriented applications.",
    long_description = read("README.md"),
    long_description_content_type = "text/markdown",
    author = "Paul Bryan",
    author_email = "pbryan@anode.ca",
    classifiers = classifiers,
    url = "https://github.com/roax/roax",
    packages = ["roax"],
    package_dir = {"": "src"},
    python_requires = ">= 3.6",
    install_requires = install_requires,
    tests_require = tests_require,
    keywords = "wsgi framework resource openapi",
    test_suite = "tests",
    cmdclass = {"test": test},
)
