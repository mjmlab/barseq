#!/usr/bin/env python3

"""
Script for Pytest setup

"""

import pytest
import shutil
import os
from pathlib import Path


__author__ = "Emanuel Burgos"
__email__ = "eburgos@wisc.edu"


@pytest.fixture(scope="session")
def temp_dir(tmp_path_factory: Path, request):
    """
    Function for creating a temporary directory to store test data.

    :param tmp_path_factory: pathlib.Path instance, dependent on os
    :param request:
    :return get_temp_path: inner function for returning path of file.
    """
    # Create temporary directory
    tmpdir = tmp_path_factory.mktemp("test")
    # Copy test data into temp directory
    shutil.copytree("barseq/tests/data", tmpdir.joinpath("data"))
    def get_tmp_path(filename=[]) -> str:
        """
        Getter for file path in tmpdir
        :param filename: filename as string
        :return new_path: path for file
        """
        return tmpdir.joinpath(*filename)

    def tear_down():
        """
        Executes when tests are done. Deletes temporary directory
        """
        shutil.rmtree(tmpdir)
        # Check that tmpdir was deleted
        assert not os.path.exists(tmpdir.joinpath("data"))
        assert not os.path.exists(tmpdir)

    request.addfinalizer(tear_down)
    return get_tmp_path




