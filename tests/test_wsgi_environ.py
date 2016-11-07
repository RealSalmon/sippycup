import urlparse
from StringIO import StringIO
from sippycup.wsgienviron import WsgiEnviron
from utils import get_apigr


def test_wsgi_environ_basic():
    tests = {
        'REQUEST_METHOD': 'GET',
        'SCRIPT_NAME': '/testing',
        'PATH_INFO': '/',
        'QUERY_STRING':  None,
        'CONTENT_TYPE': 'text/plain',
        'CONTENT_LENGTH': '0',
        'SERVER_NAME':  'testing.fogbutter.com',
        'SERVER_PORT': '443',
        'SERVER_PROTOCOL': 'HTTP/1.1',
        'wsgi.version': (1, 0),
        'wsgi.url_scheme': 'https',
        'wsgi.errors': '',
        'wsgi.multiprocess': False,
        'wsgi.multithread': False,
        'wsgi.run_once': False
    }

    request = get_apigr()
    request['headers']['Content-Type'] = 'text/plain'
    environ = WsgiEnviron(request).environ
    for key, value in tests.iteritems():
        print 'testing {0} key in WSGI environment'.format(key)
        assert environ[key] == value


def test_wsgi_environ_body():
    body = StringIO('here i am...')
    request = get_apigr()
    request['body'] = body.getvalue()
    environ = WsgiEnviron(request).environ
    assert environ['wsgi.input'].getvalue() == body.getvalue()
    assert environ['CONTENT_LENGTH'] == str(len(request['body']))


def test_wsgi_environ_query_string():
    request = get_apigr()
    request['queryStringParameters'] = {
        'param1': 'simple',
        'param2': 'needs encoding'
    }
    environ = WsgiEnviron(request).environ
    qs = urlparse.parse_qs(environ['QUERY_STRING'])
    assert qs['param1'][0] == 'simple'
    assert qs['param2'][0] == 'needs encoding'


def test_wsgi_environ_headers():
    tests = {
        'Via': '1.1 a536f7c9dbedc2b462a158901fcd8254.cloudfront.net (CloudFront)',
        'Accept-Language': 'en-US,en;q=0.8',
        'CloudFront-Is-Desktop-Viewer': 'true',
        'CloudFront-Is-SmartTV-Viewer': 'false',
        'CloudFront-Is-Mobile-Viewer': 'false',
        'X-Forwarded-For': '104.56.41.168, 54.240.159.59',
        'CloudFront-Viewer-Country': 'US',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Upgrade-Insecure-Requests': '1',
        'X-Forwarded-Port': '443',
        'Host': 'testing.fogbutter.com',
        'X-Forwarded-Proto': 'https',
        'X-Amz-Cf-Id': '03xj4hdvvnK7SX_cVWC2YOLVzl-H-UOX1FfBFcopVr5RYogDGbD6sw==',
        'CloudFront-Is-Tablet-Viewer': 'false',
        'Cache-Control': 'max-age=0',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
        'CloudFront-Forwarded-Proto': 'https',
        'Accept-Encoding': 'gzip, deflate, sdch, br'
    }
    request = get_apigr()
    environ = WsgiEnviron(request).environ
    for key, value in tests.iteritems():
        hkey = 'HTTP_{0}'.format(key.upper().replace('-', '_'))
        print 'testing for presence of {0} header in WSGI environment'.format(
            hkey
        )
        assert environ[hkey] == value

"""
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
    assert response['statusCode'] == e.description
    assert response['body'] == json.dumps(str(e))


def test_method_not_allowed():
    request = {'path': '/test/json/', 'httpMethod': 'GET'}
    response = app.run(request, None)
    e = MethodNotAllowed()
    assert response['headers']['Content-Type'] == 'application/json'
    assert response['statusCode'] == e.description
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

"""
