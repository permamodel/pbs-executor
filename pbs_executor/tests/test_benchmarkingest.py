"""Tests for the BenchmarkIngestTool class."""

import os
import shutil
from nose.tools import assert_true, assert_equal
from pbs_executor.ingest import BenchmarkIngestTool
from . import (ingest_file, benchmark_file, log_file, tmp_dir,
               link_dir, make_benchmark_files)


def setup_module():
    make_benchmark_files()
    os.mkdir(tmp_dir)


def teardown_module():
    shutil.rmtree(tmp_dir)
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
