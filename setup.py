#!/usr/bin/env python3

import sys
from glob import glob
from setuptools import *

__author__ = "Emanuel Burgos"
__email__ = "eburgos@wisc.edu"

try:
    if sys.version_info.major < 3:
        print("Barseq needs Python version of 3 or higher.")
        sys.exit(1)
except Exception:
    print("Could not figure out your python version.")

# Long description from README
with open("README.md", "r") as f:
    _long_description = f.read()

# Current Version
with open("VERSION", "r") as f:
    __version__ = f.readline().split()[-1]

# Required packages
__requirements__ = [d.strip("\n") for d in open("requirements.txt", "r")]


def main():
    setup(
        name="barseq",
        version=__version__,
        description="Analysis of barseq data.",
        long_description=_long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/mjmlab/barseq",
        author="Emanuel Burgos",
        author_email="eburgos@wisc.edu",
        license="BSD",
        scripts=glob("bin/*"),
        tests_require=["pytest"],
        install_requires=__requirements__,
        packages=find_packages(),
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Environment :: MacOS X",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: BSD License",
            "Programming Language :: Python :: 3",
            "Topic :: Scientific/Engineering :: Bio-Informatics",
        ],
        zip_safe=False)


if __name__ == "__main__":
    main()
