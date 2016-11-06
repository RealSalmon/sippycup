import json
from werkzeug.exceptions import MethodNotAllowed, NotFound
from sippycup import SippyCup

app = SippyCup()


@app.route('/test/hello/<string:name>')
@app.mimetype('text/plain')
def hello_world(name):
    return 'Hello, {0}!'.format(name)


@app.route('/test/json/', methods=['POST'])
def hello_json():
    return app.request


@app.route('/')
def index():
    return 'ohai!'


def test_not_found():
    request = {'path': '/garbonzo', 'httpMethod': 'GET'}
    response = app.run(request, None)
    e = NotFound()
    assert response['headers']['Content-Type'] == 'application/json'
    assert response['statusCode'] == e.code
    assert response['body'] == json.dumps(str(e))


def test_method_not_allowed():
    request = {'path': '/test/json/', 'httpMethod': 'GET'}
    response = app.run(request, None)
    e = MethodNotAllowed()
    assert response['headers']['Content-Type'] == 'application/json'
    assert response['statusCode'] == e.code
    assert response['body'] == json.dumps(str(e))


def test_hello_json():
    request = {'path': '/test/json/', 'httpMethod': 'POST'}
    response = app.run(request, None)
    assert response['headers']['Content-Type'] == 'application/json'
    assert response['statusCode'] == 200
    assert response['body'] == json.dumps(request)


def test_hello_world():
    request = {'path': '/test/hello/sippycup', 'httpMethod': 'GET'}
    response = app.run(request, None)
    assert response['headers']['Content-Type'] == 'text/plain'
    assert response['body'] == 'Hello, sippycup!'


def test_index():
    path = '/'
    request = {'path': path, 'httpMethod': 'GET'}
    response = app.run(request, None)
    assert response['headers']['Content-Type'] == 'application/json'
    assert response['body'] == json.dumps('ohai!')
