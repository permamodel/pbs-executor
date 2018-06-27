"""Tests for the BenchmarkIngestTool class."""

import os
import shutil
from nose.tools import assert_true, assert_false, assert_equal
from pbs_executor.ingest import BenchmarkIngestTool
from . import (ingest_file, benchmark_file, log_file, tmp_dir,
               link_dir, make_benchmark_files)


def setup_module():
    make_benchmark_files()
    os.mkdir(tmp_dir)


def teardown_module():
    shutil.rmtree(tmp_dir)
    if os.path.exists(link_dir):
        shutil.rmtree(link_dir)
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
    x.dest_dir = tmp_dir
    assert_equal(x.dest_dir, tmp_dir)


def test_set_link_dir():
    x = BenchmarkIngestTool()
    x.link_dir = link_dir
    assert_equal(x.link_dir, link_dir)


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
    f.data = 'foo'
    x.move()
    assert_true(os.path.isfile(os.path.join(tmp_dir,
                                            f.data,
                                            x.study_name,
                                            f.name)))
    assert_true(os.path.islink(os.path.join(link_dir,
                                            x.study_name,
                                            f.name)))
    assert_true(os.path.isfile(log_file))


def test_move_file_exists():
    make_benchmark_files()
    x = BenchmarkIngestTool()
    x.load(ingest_file)
    # x.verify()  # verify will clobber my simple test file
    f = x.ingest_files[0]
    f.is_verified = True
    f.data = 'foo'
    x.move()
    assert_true(os.path.isfile(os.path.join(tmp_dir,
                                            f.data,
                                            x.study_name,
                                            f.name)))
    assert_true(os.path.islink(os.path.join(link_dir,
                                            x.study_name,
                                            f.name)))
    assert_true(os.path.isfile(log_file))
