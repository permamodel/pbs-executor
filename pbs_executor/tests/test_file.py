"""Tests for the file module."""

import os
from nose.tools import assert_true
from pbs_executor.file import IngestFile, Logger
from . import log_file


regions_file_nc = 'basins_0.5x0.5.nc'


def setup_module():
    pass


def teardown_module():
    for f in [log_file]:
        try:
            os.remove(f)
        except:
            pass


def test_ingestfile_no_params():
    x = IngestFile()
    assert_true(isinstance(x, IngestFile))


def test_ingestfile_one_param():
    x = IngestFile(regions_file_nc)
    assert_true(x.name, regions_file_nc)


def test_ingestfile_set_name():
    x = IngestFile()
    x.name = regions_file_nc
    assert_true(x.name, regions_file_nc)


def test_logger_init():
    x = Logger()
    assert_true(isinstance(x, Logger))
    assert_true(os.path.isfile(log_file))


def test_logger_add():
    x = Logger()
    len0 = len(x.data)
    x.add('foo')
    assert_true(len(x.data) > len0)
    assert_true(os.path.isfile(log_file))


def test_logger_write():
    x = Logger()
    x.write()
    assert_true(os.path.isfile(log_file))
