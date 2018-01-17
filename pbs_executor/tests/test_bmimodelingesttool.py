"""Tests for the BmiModelIngestTool class."""

import os
import shutil
from nose.tools import raises, assert_true, assert_equal, assert_is_none
from permafrost_benchmark_system.bmi_ingest import BmiModelIngestTool
from . import (ingest_file, model_file, log_file, tmp_dir,
               make_test_files)


def setup_module():
    make_test_files()
    os.mkdir(tmp_dir)


def teardown_module():
    shutil.rmtree(tmp_dir)
    for f in [ingest_file, model_file, log_file]:
        try:
            os.remove(f)
        except:
            pass


def test_init():
    x = BmiModelIngestTool()
    assert_true(isinstance(x, BmiModelIngestTool))


def test_get_component_name():
    x = BmiModelIngestTool()
    assert_equal(x.get_component_name(), BmiModelIngestTool._component_name)


def test_initialize():
    x = BmiModelIngestTool()
    x.initialize(ingest_file)
    assert_equal(x._tool.ingest_files[0].name, model_file)


@raises(TypeError)
def test_initialize_no_args():
    x = BmiModelIngestTool()
    x.initialize()


def test_update():
    x = BmiModelIngestTool()
    x.initialize(ingest_file)
    x.update()
    assert_true(os.path.isfile(log_file))


def test_update_until():
    x = BmiModelIngestTool()
    x.initialize(ingest_file)
    end_time = 5.0
    x.update_until(end_time)
    assert_true(os.path.isfile(log_file))


def test_finalize():
    x = BmiModelIngestTool()
    x.finalize()
    assert_is_none(x._tool)


def test_get_input_var_names():
    x = BmiModelIngestTool()
    assert_equal(x.get_input_var_names(), ())


def test_get_output_var_names():
    x = BmiModelIngestTool()
    assert_equal(x.get_output_var_names(), ())


def test_get_start_time():
    x = BmiModelIngestTool()
    assert_equal(x.get_start_time(), 0.0)


def test_get_end_time():
    x = BmiModelIngestTool()
    assert_equal(x.get_end_time(), 1.0)


def test_get_current_time():
    x = BmiModelIngestTool()
    assert_equal(x.get_current_time(), x.get_start_time())


def test_get_time_step():
    x = BmiModelIngestTool()
    assert_equal(x.get_time_step(), 1.0)


def test_get_time_units():
    x = BmiModelIngestTool()
    assert_equal(x.get_time_units(), 's')
