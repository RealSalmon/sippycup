import json
from datetime import date, datetime
from werkzeug.routing import NotFound, MethodNotAllowed
from sippycup import SippyCup
from utils import get_apigr

app = SippyCup()


@app.route('/hello/<string:name>')
@app.route('/hello/', methods=['GET'])
@app.mimetype('text/plain')
def hello_world(name='World'):
    return 'Hello, {0}!'.format(name)


@app.route('/json/')
def json_data():
    return {
        'ohai': 'there',
        'date': date(2016, 1, 1),
        'datetime': datetime(2016, 1, 1, 0, 0, 0, 0)
    }


@app.route('/redirect/')
def redirect():
    app.response.redirect('/going/places', 301)


def test_redirect():
    r = get_apigr()
    r['path'] = '/redirect/'
    response = app.run(r, None)
    print(response)
    assert response['statusCode'] == 301
    assert response['headers']['Location'] == '/going/places'


def test_return_string_default():
    r = get_apigr()
    r['path'] = '/hello/'
    response = app.run(r, None)

    assert 'statusCode' in response
    assert response['statusCode'] == 200
    assert 'Content-Type' in response['headers']
    assert response['headers']['Content-Type'] == 'text/plain'
    assert 'body' in response
    assert response['body'] == 'Hello, World!'


def test_return_string_param():
    r = get_apigr()
    r['path'] = '/hello/SippyCup'
    response = app.run(r, None)

    assert 'statusCode' in response
    assert response['statusCode'] == 200
    assert 'Content-Type' in response['headers']
    assert response['headers']['Content-Type'] == 'text/plain'
    assert 'body' in response
    assert response['body'] == 'Hello, SippyCup!'


def test_redirect_slash():
    r = get_apigr()
    r['path'] = '/hello'
    response = app.run(r, None)
    assert response['statusCode'] == 302
    assert 'Location' in response['headers']
    assert response['headers']['Location'] == \
        'https://testing.fogbutter.com/testing/hello/'


def test_json():
    r = get_apigr()
    r['path'] = '/json/'
    response = app.run(r, None)
    assert response['headers']['Content-Type'] == 'application/json'
    assert json.loads(response['body']) == {
        'ohai': 'there',
        'date': '2016-01-01',
        'datetime': '2016-01-01T00:00:00'
    }


def test_404():
    r = get_apigr()
    r['path'] = '/garbonzo/'
    response = app.run(r, None)
    assert response['statusCode'] == NotFound.code
    assert response['headers']['Content-Type'] == 'text/plain'
    assert response['body'] == NotFound.description


def test_405():
    r = get_apigr()
    r['path'] = '/hello/'
    r['httpMethod'] = 'POST'
    response = app.run(r, None)
    assert response['statusCode'] == MethodNotAllowed.code
    assert response['headers']['Content-Type'] == 'text/plain'
    assert response['body'] == MethodNotAllowed.description
