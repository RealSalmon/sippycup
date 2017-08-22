from sippycup import SippyCupResponse


def test_response_init_state():
    response = SippyCupResponse()
    assert response.status == '200 OK'
    assert response.headers == []
    assert getattr(response.body, 'write')
    assert callable(getattr(response.body, 'write'))


def test_response_call():
    response = SippyCupResponse()
    result = response('500 Error', [('Content-Type', 'text/plain')])
    assert callable(response)
    result('ohai!')
    assert response.body.getvalue() == 'ohai!'
    assert response.status == '500 Error'
    assert len(response.headers) == 1
    assert response.headers == [('Content-Type', 'text/plain')]


def test_response_apigr_headers():
    response = SippyCupResponse()
    response(301, [('Location', 'https://ben.fogbutter.com/')])
    apigr = response.apigr()
    assert 'headers' in apigr
    assert apigr['headers'] == {'Location': 'https://ben.fogbutter.com/'}


def test_response_apigr_status():
    response = SippyCupResponse()
    response('500 Error', [])
    apigr = response.apigr()
    assert 'statusCode' in apigr
    assert apigr['statusCode'] == 500


def test_response_apigr_body():
    response = SippyCupResponse()
    result = response('200 OK', [('Content-Type', 'text/plain')])
    result('ohai!')
    apigr = response.apigr()
    assert 'body' in apigr
    assert apigr['body'] == 'ohai!'


def test_response_cookies():
    response = SippyCupResponse()
    result = response('200 OK', [
        ('Content-Type', 'text/plain'),
        ('Set-Cookie', 'something'),
        ('Set-Cookie', 'something'),
        ('Set-Cookie', 'something')
    ])
    result('ohai!')
    apigr = response.apigr()
    assert len([x for x in apigr['headers'] if x.lower() == 'set-cookie']) == 3
