"""Tests for the verify module, aka the PBS Verification Tool (VerT)."""

import os
from nose.tools import raises, assert_true
from permafrost_benchmark_system.file import IngestFile
from permafrost_benchmark_system.verify import (VerificationTool,
                                                VerificationError)
from permafrost_benchmark_system import data_directory
from . import ingest_file, model_file, make_test_files


file_txt = 'tropics.txt'
file_nc = 'basins_0.5x0.5.nc'


def setup_module():
    make_test_files()


def teardown_module():
    for f in [ingest_file, model_file]:
        try:
            os.remove(f)
        except:
            pass


@raises(TypeError)
def test_error_init_with_no_args():
    e = VerificationError()


def test_error_init():
    e = VerificationError('foo')
    assert_true(isinstance(e, VerificationError))


@raises(TypeError)
def test_init_fails_with_no_args():
    x = VerificationTool()


def test_init():
    f = IngestFile(model_file)
    x = VerificationTool(f)
    assert_true(isinstance(x, VerificationTool))


@raises(VerificationError)
def test_is_netcdf():
    f = os.path.join(data_directory, file_txt)
    ingest_file = IngestFile(f)
    v = VerificationTool(ingest_file)
    v.is_netcdf()


@raises(VerificationError)
def test_is_netcdf3_data_model():
    f = os.path.join(data_directory, file_nc)
    ingest_file = IngestFile(f)
    v = VerificationTool(ingest_file)
    v.is_netcdf3_data_model()


def test_parse_filename():
    f = os.path.join(data_directory, file_nc)
    ingest_file = IngestFile(f)
    v = VerificationTool(ingest_file)
    v.parse_filename()
    assert_true(len(v.parts) > 0)


@raises(VerificationError)
def test_filename_has_model_name():
    f = os.path.join(data_directory, file_nc)
    ingest_file = IngestFile(f)
    v = VerificationTool(ingest_file)
    v.filename_has_model_name()


@raises(VerificationError)
def test_verify():
    f = os.path.join(data_directory, file_nc)
    ingest_file = IngestFile(f)
    v = VerificationTool(ingest_file)
    v.verify()
