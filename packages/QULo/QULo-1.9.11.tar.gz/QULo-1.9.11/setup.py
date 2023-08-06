#!/bin/env python

#######################################################################
# Copyright (C) 2015-2019 David Palao
#
# This file is part of QULo.
#
#  QULo is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  QULo is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with QULo.  If not, see <http://www.gnu.org/licenses/>.
#
#######################################################################

from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(name="QULo",
    use_scm_version={"version_scheme": "post-release"},
    setup_requires=['setuptools_scm'],
    description="A package to collect basic performance data from clusters",
    long_description=long_description,
    author="David Palao",
    author_email="palao@csc.uni-frankfurt.de",
    url="https://itp.uni-frankfurt.de/~palao/software/QULo",
    license='GNU General Public License (GPLv3)',
    packages=find_packages(),
    provides=["qulo"],
    install_requires=["psutil"],
    platforms=['GNU/Linux'],
    entry_points={'console_scripts': [
        "qulod = qulo.qulod:main",
        "qagent = qulo.qagent:main",
        "qmaster = qulo.qmaster:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Environment :: No Input/Output (Daemon)",
        "Framework :: AsyncIO",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: System :: Monitoring",
    ],
    test_suite="tests",
)
