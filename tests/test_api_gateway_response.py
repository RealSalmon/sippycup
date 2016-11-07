from werkzeug.wrappers import Response
from sippycup.responses import SippyCupApiGatewayResponse

r = Response()
r.status_code = 200
r.set_data('I am here')
r.set_cookie('ohai', 'there')
r.headers['Content-Type'] = 'text/plain'
sr = SippyCupApiGatewayResponse(r)


def test_response_body():
    assert sr.body == 'I am here'


def test_response_status():
    assert sr.statusCode == 200


def test_response_headers():
    assert type(sr.headers) is dict
    assert 'Content-Type' in sr.headers
    assert sr.headers['Content-Type'] =='text/plain'


def test_response_cookies():
    print(sr.headers['Set-Cookie'])
    assert 'Set-Cookie' in sr.headers
    assert sr.headers['Set-Cookie'] == 'ohai=there; Path=/'


def test_response_as_dict():
    sd = dict(sr)
    assert 'headers' in sd
    assert sd['headers']['Content-Type'] == 'text/plain'
    assert 'body' in sd
    assert sd['body'] == 'I am here'
    assert 'statusCode' in sd
    assert sd['statusCode'] == 200
