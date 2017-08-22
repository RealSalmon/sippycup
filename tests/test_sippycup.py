from flask import Flask, Response, make_response, redirect
from sippycup import sippycup
from tests.utils import get_apigr

app = Flask(__name__)


@app.route('/test/plain')
def plain():
    return Response('ohai!', content_type='text/plain')


@app.route('/test/cookies')
def cookies():
    r = make_response(redirect('/test/plain'))
    r.set_cookie('a', '1')
    r.set_cookie('b', '2')
    r.set_cookie('c', '3')
    return r


def test_response_body():
    event = get_apigr()
    event['path'] = '/test/plain'
    result = sippycup(app, event)
    assert 'body' in result
    assert result['body'] == 'ohai!'


def test_response_headers():
    event = get_apigr()
    event['path'] = '/test/plain'
    result = sippycup(app, event)
    assert 'headers' in result
    assert 'Content-Type' in result['headers']
    assert result['headers']['Content-Type'] == 'text/plain'
    assert result['headers']['Content-Length'] == '5'


def test_response_status():
    event = get_apigr()
    event['path'] = '/test/plain'
    result = sippycup(app, event)
    assert 'statusCode' in result
    assert result['statusCode'] == 200


def test_response_cookies():
    event = get_apigr()
    event['path'] = '/test/cookies'
    result = sippycup(app, event)
    assert len([x for x in result['headers'] if x.lower() == 'set-cookie']) == 3
