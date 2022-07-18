import unittest
from io import BytesIO, StringIO
import cgi

urlencode_data = "key2=value2x&key3=value3&key4=value4"
formdata_environ = {
    'CONTENT_LENGTH':   str(len(urlencode_data)),
    'CONTENT_TYPE':     'application/x-www-form-urlencoded',
    'QUERY_STRING':     'key1=value1&key2=value2x',
    'REQUEST_METHOD':   'POST',
}


def gen_result(data: str, environ: dict) -> dict:
    fake_stdin = StringIO(data)
    fake_stdin.seek(0)
    form = cgi.FieldStorage(fp=fake_stdin, environ=environ)
    result = {}
    for k, v in dict(form).items():
        result[k] = type(v) is list and form.getlist(k) or v.value
    return result


def test_prepare_log():
    assert False


def test_load_cfg():
    assert False


def test_sanitize():
    assert False


def test_hook():
    assert False
