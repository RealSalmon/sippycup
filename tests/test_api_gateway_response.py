from sippycup.responses import SippyCupResponse

r = SippyCupResponse()
r.status_code = 200
r.headers['Content-Type'] = 'text/plain'
r.set_data('I am here')
r.set_cookie('ohai', 'there')


def test_response_body():
    assert r.apigr['body'] == 'I am here'


def test_response_status():
    assert r.apigr['statusCode'] == 200


def test_response_headers():
    assert type(r.apigr['headers']) is dict
    assert 'Content-Type' in r.headers
    assert r.apigr['headers']['Content-Type'] =='text/plain'


def test_response_cookies():
    print(r.apigr['headers']['Set-Cookie'])
    assert 'Set-Cookie' in r.apigr['headers']
    assert r.apigr['headers']['Set-Cookie'] == 'ohai=there; Path=/'
