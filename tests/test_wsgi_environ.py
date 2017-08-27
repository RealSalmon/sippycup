from sys import stderr
from sippycup import WsgiEnviron
from tests.utils import get_apigr
try:
    import urlparse
    from StringIO import StringIO
except ImportError:
    from urllib import parse as urlparse
    from io import StringIO


def test_wsgi_environ_basic():
    tests = {
        'REQUEST_METHOD': 'GET',
        'SCRIPT_NAME': '/testing',
        'PATH_INFO': '/',
        'QUERY_STRING':  '',
        'CONTENT_TYPE': 'text/plain',
        'CONTENT_LENGTH': '0',
        'SERVER_NAME':  'testing.fogbutter.com',
        'SERVER_PORT': '443',
        'SERVER_PROTOCOL': 'HTTP/1.1',
        'wsgi.version': (1, 0),
        'wsgi.url_scheme': 'https',
        'wsgi.errors': stderr,
        'wsgi.multiprocess': False,
        'wsgi.multithread': False,
        'wsgi.run_once': False,
        'apigateway': True
    }

    request = get_apigr()
    request['headers']['Content-Type'] = 'text/plain'
    environ = WsgiEnviron(request).environ
    for key, value in tests.items():
        print('testing {0} key in WSGI environment'.format(key))
        assert environ[key] == value


def test_script_name_is_script_name():
    request = get_apigr()
    wsgi = WsgiEnviron(request)
    assert wsgi.script_name == wsgi.environ['SCRIPT_NAME']


def test_wsgi_script_name_root():
    request = get_apigr()
    request['requestContext']['resourcePath'] = '/'
    request['path'] = '/testing/'
    wsgi = WsgiEnviron(request)
    assert wsgi.script_name == '/testing'


def test_wsgi_script_name_root_mapped():
    request = get_apigr()
    request['requestContext']['resourcePath'] = '/'
    request['path'] = '/'
    request['stageVariables']['SIPPYCUP_SCRIPT_NAME_BASE'] = '/'
    wsgi = WsgiEnviron(request)
    assert wsgi.script_name == ''


def test_wsgi_script_name_root_proxy():
    request = get_apigr()
    request['requestContext']['resourcePath'] = '/{proxy+}'
    request['path'] = '/testing/some/params'
    wsgi = WsgiEnviron(request)
    assert wsgi.script_name == '/testing'


def test_wsgi_script_name_root_proxy_mapped():
    request = get_apigr()
    request['requestContext']['resourcePath'] = '/{proxy+}'
    request['path'] = '/some/params'
    request['stageVariables']['SIPPYCUP_SCRIPT_NAME_BASE'] = '/'
    wsgi = WsgiEnviron(request)
    assert wsgi.script_name == ''


def test_wsgi_script_name_nested():
    request = get_apigr()
    request['requestContext']['resourcePath'] = '/nested'
    request['path'] = '/testing/nested/'
    wsgi = WsgiEnviron(request)
    assert wsgi.script_name == '/testing/nested'


def test_wsgi_script_name_nested_mapped():
    request = get_apigr()
    request['requestContext']['resourcePath'] = '/nested'
    request['path'] = '/nested/'
    request['stageVariables']['SIPPYCUP_SCRIPT_NAME_BASE'] = '/'
    wsgi = WsgiEnviron(request)
    assert wsgi.script_name == '/nested'


def test_wsgi_script_name_nested_proxy():
    request = get_apigr()
    request['requestContext']['resourcePath'] = '/nested/{proxy+}'
    request['path'] = '/testing/nested/some/params'
    wsgi = WsgiEnviron(request)
    assert wsgi.script_name == '/testing/nested'


def test_wsgi_script_name_nested_proxy_mapped():
    request = get_apigr()
    request['requestContext']['resourcePath'] = '/nested/{proxy+}'
    request['path'] = '/nested/some/params'
    request['stageVariables']['SIPPYCUP_SCRIPT_NAME_BASE'] = '/'
    wsgi = WsgiEnviron(request)
    assert wsgi.script_name == '/nested'


def test_wsgi_path_info_root():
    request = get_apigr()
    request['requestContext']['resourcePath'] = '/'
    request['path'] = '/'
    environ = WsgiEnviron(request).environ
    assert environ['PATH_INFO'] == '/'


def test_wsgi_path_info_root_proxy():
    request = get_apigr()
    request['requestContext']['resourcePath'] = '/{proxy+}'
    request['path'] = '/'
    environ = WsgiEnviron(request).environ
    assert environ['PATH_INFO'] == '/'


def test_wsgi_path_info_root_proxy_pathargs():
    request = get_apigr()
    request['requestContext']['resourcePath'] = '/{proxy+}'
    request['path'] = '/ohai'
    environ = WsgiEnviron(request).environ
    assert environ['PATH_INFO'] == '/ohai'


def test_wsgi_path_info_nested():
    request = get_apigr()
    request['requestContext']['resourcePath'] = '/nested'
    request['path'] = '/nested'
    environ = WsgiEnviron(request).environ
    assert environ['PATH_INFO'] == ''

def test_wsgi_path_info_nested_proxy():
    request = get_apigr()
    request['requestContext']['resourcePath'] = '/nested/{proxy+}'
    request['path'] = '/nested'
    environ = WsgiEnviron(request).environ
    assert environ['PATH_INFO'] == ''


def test_wsgi_path_info_nested_proxy_pathargs():
    request = get_apigr()
    request['requestContext']['resourcePath'] = '/nested/{proxy+}'
    request['path'] = '/nested/ohai'
    environ = WsgiEnviron(request).environ
    assert environ['PATH_INFO'] == '/ohai'


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
    for key, value in tests.items():
        hkey = 'HTTP_{0}'.format(key.upper().replace('-', '_'))
        print('testing for presence of {0} header in WSGI environment'.format(
            hkey
        ))
        assert environ[hkey] == value


def test_wsgi_environ_stage_vars():
    request = get_apigr()
    environ = WsgiEnviron(request).environ
    assert 'apigateway.stageVariables' in environ
    assert environ['apigateway.stageVariables'] == {
            "ben": "was-here",
            "so_was": "red"
    }


def test_empty_stage_vars():
    request = get_apigr()
    request['stageVariables'] = None
    environ = WsgiEnviron(request).environ
    assert type(environ['apigateway.stageVariables']) == dict
