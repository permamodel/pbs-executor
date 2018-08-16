"""Tests for the BenchmarkIngestTool class."""

import os
import shutil
from nose.tools import assert_true, assert_false, assert_equal
from pbs_executor.ingest import BenchmarkIngestTool
from pbs_executor.utils import is_in_file
from . import (ingest_file, benchmark_file, log_file, data_dir,
               data_link_dir, make_benchmark_files)


variable_name = 'lai'


def setup_module():
    make_benchmark_files()
    os.mkdir(data_dir)


def teardown_module():
    shutil.rmtree(data_dir)
    if os.path.exists(data_link_dir):
        shutil.rmtree(data_link_dir)
    for f in [ingest_file, benchmark_file, log_file]:
        try:
            os.remove(f)
        except:
            pass


def test_init():
    x = BenchmarkIngestTool()
    assert_true(isinstance(x, BenchmarkIngestTool))


def test_load():
    x = BenchmarkIngestTool()
    x.load(ingest_file)
    assert_equal(x.ingest_files[0].name, benchmark_file)


def test_init_with_ingest_file():
    x = BenchmarkIngestTool(ingest_file=ingest_file)
    assert_true(isinstance(x, BenchmarkIngestTool))
    assert_equal(x.ingest_files[0].name, benchmark_file)


def test_logger():
    x = BenchmarkIngestTool()
    assert_true(os.path.isfile(log_file))


def test_set_dest_dir():
    x = BenchmarkIngestTool()
    x.dest_dir = data_dir
    assert_equal(x.dest_dir, data_dir)


def test_set_link_dir():
    x = BenchmarkIngestTool()
    x.link_dir = data_link_dir
    assert_equal(x.link_dir, data_link_dir)


def test_verify():
    x = BenchmarkIngestTool()
    x.load(ingest_file)
    x.verify()
    assert_false(os.path.isfile(benchmark_file))
    assert_true(os.path.isfile(log_file))


def test_move_file_new():
    make_benchmark_files()
    x = BenchmarkIngestTool()
    x.load(ingest_file)
    # x.verify()  # verify will clobber my simple test file
    f = x.ingest_files[0]
    f.is_verified = True
    f.data = variable_name
    x.move()
    assert_true(os.path.isfile(os.path.join(data_dir,
                                            f.data,
                                            x.source_name,
                                            f.name)))
    link_name = '{}.{}'.format(f.name, x.source_name)
    assert_true(os.path.islink(os.path.join(data_link_dir,
                                            x.project_name,
                                            link_name)))
    assert_true(os.path.isfile(log_file))


def test_move_file_exists():
    make_benchmark_files()
    x = BenchmarkIngestTool()
    x.load(ingest_file)
    # x.verify()  # verify will clobber my simple test file
    f = x.ingest_files[0]
    f.is_verified = True
    f.data = variable_name
    x.move()
    assert_true(os.path.isfile(os.path.join(data_dir,
                                            f.data,
                                            x.source_name,
                                            f.name)))
    link_name = '{}.{}'.format(f.name, x.source_name)
    assert_true(os.path.islink(os.path.join(data_link_dir,
                                            x.project_name,
                                            link_name)))
    assert_true(os.path.isfile(log_file))
    assert_true(is_in_file(log_file, 'File Exists'))


def test_move_file_exists_overwrite():
    make_benchmark_files()
    x = BenchmarkIngestTool()
    x.load(ingest_file)
    x.overwrite_files = True
    # x.verify()  # verify will clobber my simple test file
    f = x.ingest_files[0]
    f.is_verified = True
    f.data = variable_name
    x.move()
    assert_true(os.path.isfile(os.path.join(data_dir,
                                            f.data,
                                            x.source_name,
                                            f.name)))
    link_name = '{}.{}'.format(f.name, x.source_name)
    assert_true(os.path.islink(os.path.join(data_link_dir,
                                            x.project_name,
                                            link_name)))
    assert_true(os.path.isfile(log_file))
    assert_false(is_in_file(log_file, 'File Exists'))
