"""Tests for the ModelIngestTool class."""

import os
import shutil
from nose.tools import assert_true, assert_false, assert_equal
from pbs_executor.ingest import ModelIngestTool
from pbs_executor.utils import is_in_file, check_permissions
from . import (ingest_file, model_file, log_file, models_dir,
               models_link_dir, make_model_files)


model_name = 'SiBCASA'
permissions = '775'


def setup_module():
    make_model_files()
    os.mkdir(models_dir)


def teardown_module():
    shutil.rmtree(models_dir)
    if os.path.exists(models_link_dir):
        shutil.rmtree(models_link_dir)
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
    x.dest_dir = models_dir
    assert_equal(x.dest_dir, models_dir)


def test_verify():
    x = ModelIngestTool()
    x.load(ingest_file)
    x.verify()
    assert_false(os.path.isfile(model_file))
    assert_true(os.path.isfile(log_file))


def test_move_file_new():
    make_model_files()
    x = ModelIngestTool()
    x.load(ingest_file)
    # x.verify()  # verify will clobber my simple test file
    f = x.ingest_files[0]
    f.is_verified = True
    f.data = model_name
    x.move()
    source_dir = os.path.join(models_dir, f.data)
    assert_true(os.path.isfile(os.path.join(source_dir, f.name)))
    assert_true(check_permissions(source_dir, permissions))
    assert_true(os.path.islink(os.path.join(models_link_dir,
                                            x.project_name, f.name)))
    assert_true(os.path.isfile(log_file))


# Note that an exception isn't raised, but a message is written to the
# log file.
def test_move_file_exists():
    make_model_files()
    x = ModelIngestTool()
    x.load(ingest_file)
    # x.verify()  # verify will clobber my simple test file
    f = x.ingest_files[0]
    f.is_verified = True
    f.data = model_name
    x.move()
    source_dir = os.path.join(models_dir, f.data)
    assert_true(os.path.isfile(os.path.join(source_dir, f.name)))
    assert_true(check_permissions(source_dir, permissions))
    assert_true(os.path.islink(os.path.join(models_link_dir,
                                            x.project_name, f.name)))
    assert_true(os.path.isfile(log_file))
    assert_true(is_in_file(log_file, 'File Exists'))


def test_move_file_exists_overwrite():
    make_model_files()
    x = ModelIngestTool()
    x.load(ingest_file)
    x.overwrite_files = True
    # x.verify()  # verify will clobber my simple test file
    f = x.ingest_files[0]
    f.is_verified = True
    f.data = model_name
    x.move()
    source_dir = os.path.join(models_dir, f.data)
    assert_true(os.path.isfile(os.path.join(source_dir, f.name)))
    assert_true(check_permissions(source_dir, permissions))
    assert_true(os.path.islink(os.path.join(models_link_dir,
                                            x.project_name, f.name)))
    assert_true(os.path.isfile(log_file))
    assert_false(is_in_file(log_file, 'File Exists'))
