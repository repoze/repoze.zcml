##############################################################################
#
# Copyright (c) 2009 Agendaless Consulting and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the BSD-like license at
# http://www.repoze.org/LICENSE.txt.  A copy of the license should accompany
# this distribution.  THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL
# EXPRESS OR IMPLIED WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND
# FITNESS FOR A PARTICULAR PURPOSE
#
##############################################################################

__version__ = '1.0b1'

import os

from setuptools import find_packages
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

def _read_file(filename):
    try:
        with open(os.path.join(here, filename)) as f:
            return f.read()
    except IOError:  # Travis???
        return ''

README = _read_file( 'README.rst')
CHANGES = _read_file( 'CHANGES.rst')

install_requires = [
    'setuptools',
    'zope.component>=3.5.0',
    'zope.configuration',
    ]

tests_require = install_requires + ['zope.testing']

testing_extras = ['nose', 'coverage']

setup(name='repoze.zcml',
      version=__version__,
      description='Core directives for use in ZCML-based applications',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: Implementation :: CPython",
        ],
      keywords='zope zcml component architecture',
      author="Agendaless Consulting",
      author_email="repoze-dev@lists.repoze.org",
      url="http://www.repoze.org",
      license="BSD-derived (http://www.repoze.org/LICENSE.txt)",
      packages=find_packages(),
      include_package_data=True,
      namespace_packages=['repoze'],
      zip_safe=False,
      tests_require = tests_require,
      install_requires= install_requires,
      test_suite="repoze.zcml",
      entry_points = """\
      """,
      extras_require = {
        'testing': tests_require + testing_extras,
      }
)
