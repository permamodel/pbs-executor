"""Tests for the file module, minus the IlambConfigFile class."""

import os
from nose.tools import raises, assert_true, assert_equal
from permafrost_benchmark_system.file import (get_region_labels_txt,
                                              get_region_labels_ncdf,
                                              IngestFile, Logger)
from permafrost_benchmark_system import data_directory
from . import log_file


regions_file_txt = 'tropics.txt'
regions_file_txt_path = os.path.join(data_directory, regions_file_txt)
labels_txt = ['tropics', 'afritrop']
regions_file_nc = 'basins_0.5x0.5.nc'
regions_file_nc_path = os.path.join(data_directory, regions_file_nc)
labels_nc = ['amazon', 'ob', 'lena']


def setup_module():
    pass


def teardown_module():
    for f in [log_file]:
        try:
            os.remove(f)
        except:
            pass


@raises(IOError)
def test_get_region_labels_txt_path():
    get_region_labels_txt(regions_file_txt)


def test_get_region_labels_txt_type():
    x = get_region_labels_txt(regions_file_txt_path)
    assert_true(type(x), list)


def test_get_region_labels_txt_value():
    x = get_region_labels_txt(regions_file_txt_path)
    assert_equal(x, labels_txt)


@raises(IOError)
def test_get_region_labels_ncdf_path():
    get_region_labels_ncdf(regions_file_nc)


def test_get_region_labels_ncdf_type():
    x = get_region_labels_ncdf(regions_file_nc_path)
    assert_true(type(x), list)


def test_get_region_labels_ncdf_value():
    x = get_region_labels_ncdf(regions_file_nc_path)
    assert_equal(x[0:3], labels_nc)


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
