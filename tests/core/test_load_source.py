import tempfile

import json
import yaml

from flex.core import load_source


def test_native_mapping_is_passthrough():
    source = {'foo': 'bar'}
    result = load_source(source)

    assert result == source


def test_json_string():
    native = {'foo': 'bar'}
    source = json.dumps(native)
    result = load_source(source)

    assert result == native


def test_yaml_string():
    native = {'foo': 'bar'}
    source = yaml.dump(native)
    result = load_source(source)

    assert result == native


def test_json_file_object():
    native = {'foo': 'bar'}
    source = json.dumps(native)

    tmp_file = tempfile.NamedTemporaryFile(mode='r+w')
    tmp_file.write(source)
    tmp_file.file.seek(0)

    result = load_source(tmp_file.file)

    assert result == native


def test_json_file_path():
    native = {'foo': 'bar'}
    source = json.dumps(native)

    tmp_file = tempfile.NamedTemporaryFile(mode='r+w', suffix='.json')
    tmp_file.write(source)
    tmp_file.file.seek(0)

    result = load_source(tmp_file.name)

    assert result == native


def test_yaml_file_object():
    native = {'foo': 'bar'}
    source = yaml.dump(native)

    tmp_file = tempfile.NamedTemporaryFile(mode='r+w')
    tmp_file.write(source)
    tmp_file.file.seek(0)

    result = load_source(tmp_file.file)

    assert result == native


def test_yaml_file_path():
    native = {'foo': 'bar'}
    source = yaml.dump(native)

    tmp_file = tempfile.NamedTemporaryFile(mode='r+w', suffix='.yaml')
    tmp_file.write(source)
    tmp_file.file.seek(0)

    result = load_source(tmp_file.name)

    assert result == native
