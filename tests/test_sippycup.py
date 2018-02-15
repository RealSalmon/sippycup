import json
from flask import Flask, Response, make_response, redirect, request
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


@app.route('/test/query')
def query():
    return Response(request.args.get('a'), mimetype='text/plain')


@app.route('/test/post', methods=['POST'])
def post():
    return json.dumps(request.form)


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


def test_response_empty_query():
    event = get_apigr()
    event['path'] = '/test/query'
    event['queryStringParameters'] = None
    result = sippycup(app, event)
    assert result['body'] == ''


def test_response_query():
    event = get_apigr()
    event['path'] = '/test/query'
    event['queryStringParameters'] = {'a': 'ohai'}
    result = sippycup(app, event)
    assert result['body'] == 'ohai'


def test_response_post():
    event = get_apigr()
    event['path'] = '/test/post'
    event['body'] = 'a=ohai'
    event['requestContext']['httpMethod'] = 'POST'
    event['httpMethod'] = 'POST'
    event['headers']['Content-Length'] = 6
    event['headers']['Content-Type'] = 'application/x-www-form-urlencoded'
    result = sippycup(app, event)
    assert result['body'] == '{"a": "ohai"}'
