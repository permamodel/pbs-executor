"""Tests for the ModelIngestTool class."""

import os
import shutil
from nose.tools import assert_true, assert_false, assert_equal
from permafrost_benchmark_system.ingest import ModelIngestTool
from . import (ingest_file, model_file, log_file, tmp_dir, link_dir,
               make_test_files)


def setup_module():
    make_test_files()
    os.mkdir(tmp_dir)


def teardown_module():
    shutil.rmtree(tmp_dir)
    shutil.rmtree(link_dir)
    for f in [ingest_file, model_file, log_file]:
        try:
            os.remove(f)
        except:
            pass


def test_init():
    x = ModelIngestTool()
    assert_true(isinstance(x, ModelIngestTool))


def test_load():
    x = ModelIngestTool()
    x.load(ingest_file)
    assert_equal(x.ingest_files[0].name, model_file)


def test_init_with_ingest_file():
    x = ModelIngestTool(ingest_file=ingest_file)
    assert_true(isinstance(x, ModelIngestTool))
    assert_equal(x.ingest_files[0].name, model_file)


def test_logger():
    x = ModelIngestTool()
    assert_true(os.path.isfile(log_file))


def test_set_dest_dir():
    x = ModelIngestTool()
    x.dest_dir = tmp_dir
    assert_equal(x.dest_dir, tmp_dir)


def test_verify():
    x = ModelIngestTool()
    x.load(ingest_file)
    x.verify()
    assert_false(os.path.isfile(model_file))
    assert_true(os.path.isfile(log_file))


def test_move_file_new():
    make_test_files()
    x = ModelIngestTool()
    x.load(ingest_file)
    # x.verify()  # verify will clobber my simple test file
    x.ingest_files[0].is_verified = True
    x.ingest_files[0].data = 'foo'
    x.move()
    assert_true(os.path.isfile(os.path.join(tmp_dir, 'foo', model_file)))
    assert_true(os.path.isfile(log_file))


def test_move_file_exists():
    make_test_files()
    x = ModelIngestTool()
    x.load(ingest_file)
    # x.verify()  # verify will clobber my simple test file
    x.ingest_files[0].is_verified = True
    x.ingest_files[0].data = 'foo'
    x.move()
    assert_true(os.path.isfile(os.path.join(tmp_dir, 'foo', model_file)))
    assert_true(os.path.isfile(log_file))
