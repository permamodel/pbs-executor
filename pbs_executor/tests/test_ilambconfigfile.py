"""Tests for the IlambConfigFile class."""
import os
import filecmp
import numpy as np
from nose.tools import raises, assert_true, assert_false, assert_equal
from ConfigParser import SafeConfigParser
from permafrost_benchmark_system.file import IlambConfigFile
from permafrost_benchmark_system import data_directory


default_config_file = 'ilamb.cfg'
default_config_file_path = os.path.join(data_directory, default_config_file)
n_sources = 12
gpp_template_file = 'gpp.cfg.tmpl'
relationship = '"LeafAreaIndex/AVHRR"'
default_title = 'Permafrost Benchmark System'


def setup_module():
    pass


def teardown_module():
    try:
        os.remove(default_config_file)
    except:
        pass


@raises(TypeError)
def test_init_no_parameters():
    IlambConfigFile()


def test_init_string_variable():
    param = 'gpp'
    x = IlambConfigFile(param)
    assert_true(type(x.variables), tuple)


def test_init_list_variable():
    param = ['gpp']
    x = IlambConfigFile(param)
    assert_true(type(x.variables), list)


def test_init_tuple_variable():
    param = ('gpp',)
    x = IlambConfigFile(param)
    assert_true(type(x.variables), tuple)


def test_init_array_variable():
    param = np.array(('gpp',))
    x = IlambConfigFile(param)
    assert_true(type(x.variables), np.ndarray)


def test_init_multiple_variables():
    param = ('gpp', 'lai', 'le')
    x = IlambConfigFile(param)
    assert_equal(len(x.variables), len(param))


def test_config_file_default():
    param = 'gpp'
    x = IlambConfigFile(param)
    assert_equal(x.config_file, default_config_file)


def test_config_file_user():
    param = 'gpp'
    config_file = 'foo.cfg'
    x = IlambConfigFile(param, config_file=config_file)
    assert_equal(x.config_file, config_file)


def test_title_default():
    param = 'gpp'
    x = IlambConfigFile(param)
    assert_equal(x.title, default_title)


def test_title_user():
    param = 'gpp'
    title = 'ILAMB rulz!'
    x = IlambConfigFile(param, title=title)
    assert_equal(x.title, title)


def test_relationships_default():
    param = 'gpp'
    x = IlambConfigFile(param)
    assert_false(x.has_relationships)


def test_relationships_user():
    param = ['gpp', 'le']
    x = IlambConfigFile(param, relationships=True)
    assert_true(x.has_relationships)


@raises(TypeError)
def test_relationships_fails_with_fewer_than_two_variables():
    param = 'gpp'
    IlambConfigFile(param, relationships=True)


def test_get_template_file():
    param = 'gpp'
    x = IlambConfigFile(param)
    tmpl_file = x.get_template_file(param)
    assert_equal(tmpl_file, os.path.join(data_directory, gpp_template_file))


@raises(IOError)
def test_get_template_file_unknown_variable():
    param = 'foo'
    x = IlambConfigFile(param)
    x.get_template_file(param)


def test_read_method():
    param = 'gpp'
    x = IlambConfigFile(param)
    x.read(param)
    assert_true(isinstance(x.config[param], SafeConfigParser))


def test_read_method_multiple_variables():
    param = ('gpp', 'lai', 'le')
    x = IlambConfigFile(param, relationships=True)
    for var in x.variables:
        x.read(var)
        assert_true(isinstance(x.config[var], SafeConfigParser))
    assert_equal(len(param), len(x.config.keys()))


@raises(IOError)
def test_read_method_unknown_variable():
    param = 'foo'
    x = IlambConfigFile(param)
    x.read(param)


def test_get_sources():
    param = 'gpp'
    x = IlambConfigFile(param)
    x.get_sources()
    assert_equal(len(x.sources), n_sources)


def test_add_relationships():
    param = ('gpp', 'lai')
    x = IlambConfigFile(param, relationships=True)
    for var in x.variables:
        x.read(var)
    x.get_sources()
    x.add_relationships()
    rel = x.config['gpp'].get('Fluxnet-MTE', 'relationships')
    assert_equal(relationship, rel)


def test_setup():
    param = 'gpp'
    x = IlambConfigFile(param)
    x.setup()
    assert_true(isinstance(x.config[param], SafeConfigParser))


def test_setup_with_relationships():
    param = ('gpp', 'lai', 'le')
    x = IlambConfigFile(param, relationships=True)
    x.setup()
    for p in param:
        assert_true(isinstance(x.config[p], SafeConfigParser))


def test_write():
    param = 'gpp'
    x = IlambConfigFile(param)
    x.setup()
    x.write()
    assert_true(filecmp.cmp(default_config_file_path, default_config_file))
