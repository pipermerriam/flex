import tempfile
import collections

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


def test_url(httpbin):
    native = {
        'origin': '127.0.0.1',
        #'headers': {
        #    'Content-Length': '',
        #    'Accept-Encoding': 'gzip, deflate',
        #    'Host': '127.0.0.1:54634',
        #    'Accept': '*/*',
        #    'User-Agent': 'python-requests/2.4.3 CPython/2.7.8 Darwin/14.0.0',
        #    'Connection': 'keep-alive',
        #},
        'args': {},
        #'url': 'http://127.0.0.1:54634/get',
    }
    source = httpbin.url + '/get'
    result = load_source(source)
    assert isinstance(result, collections.Mapping)
    result.pop('headers')
    result.pop('url')
    assert result == native
