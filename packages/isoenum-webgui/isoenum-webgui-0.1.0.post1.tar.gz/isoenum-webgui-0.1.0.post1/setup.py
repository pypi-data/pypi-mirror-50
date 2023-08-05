#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import re
from setuptools import setup, find_packages


if sys.argv[-1] == "publish":
    os.system("python3 setup.py sdist")
    os.system("twine upload dist/*")
    sys.exit()


def readme():
    with open("README.md") as readme_file:
        return readme_file.read()


def find_version():
    with open("isoenum_webgui/__init__.py", "r") as fd:
        version = re.search(
            r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE
        ).group(1)
    if not version:
        raise RuntimeError("Cannot find version information")
    return version


REQUIRES = [
    "Flask",
    "Flask-Excel",
    "Flask-WTF",
    "docopt >= 0.6.2",
    "ctfile >= 0.1.8",
    "isoenum >= 0.4.0"
]


setup(
    name="isoenum-webgui",
    version=find_version(),
    author="Andrey Smelter",
    author_email="andrey.smelter@gmail.com",
    description="Web interface to generate NMR-specific InChI",
    keywords="InChI InChIKey isoenum isotopic enumerator",
    license="BSD",
    url="https://github.com/MoseleyBioinformaticsLab/isoenum-webgui",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    long_description=readme(),
    long_description_content_type='text/markdown',
    install_requires=REQUIRES,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)