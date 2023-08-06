#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from os.path import abspath, dirname, join
from setuptools import setup, find_packages
try: # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements


currdir = abspath(dirname(__file__))
with open(join(currdir, 'README.md')) as f:
    long_descr = f.read()

requirements = parse_requirements("requirements.txt", session=False)
setup(
  name = "recursive-compression",
  packages = find_packages(),
  author = "Alexandre D\'Hondt",
  author_email = "alexandre.dhondt@gmail.com",
  url = "https://github.com/dhondta/recursive-compression",
  version = "2.7",
  license = "AGPLv3",
  description = "Tool for recursively (de)compressing nested archives using"
                " multiple algorithms (bzip2, rar, lzma, ...)",
  long_description=long_descr,
  long_description_content_type='text/markdown',
  keywords = ["python", "tool", "recursive", "compression", "decompression",
              "bzip2", "tar", "rar", "xz", "arj", "lzma", "gzip", "7z", "zip"],
  scripts = ["rec-comp", "rec-decomp"],
  classifiers = [
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Intended Audience :: Information Technology',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Topic :: Security',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
  install_requires=[str(r.req) for r in requirements],
  python_requires = '>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*,<4',
)
