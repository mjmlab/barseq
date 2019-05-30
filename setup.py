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

# Long description
with open("README.md", "r") as f:
    _long_description = f.read()

# Current Version
with open("VERSION", "r") as f:
    __version__ = f.readline().split()[-1]

# Required dependencies
__dependencies__ = [d.strip("\n") for d in open("requirements.txt", "r")]


def main():
    setup(
        name="barseq",
        version=__version__,
        description="None",
        long_description_type="text/markdown",
        url="None",
        author="Emanuel Burgos",
        author_email="eburgos@wisc.edu",
        license="BSD",
        scripts=glob("bin/*"),
        tests_require=["pytest"],
        installation_require=None,
        packages=find_packages(),
        classifiers=[],
        zip_safe=False)


if __name__ == "__main__":
    main()
