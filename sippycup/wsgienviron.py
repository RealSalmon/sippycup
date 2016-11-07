from StringIO import StringIO
from urllib import urlencode

# https://www.python.org/dev/peps/pep-0333/


class WsgiEnviron(object):

    @property
    def body(self):
        if self.request['body'] is not None:
            return StringIO(self.request['body'])
        else:
            return None

    @property
    def content_length(self):
        if self.request['body'] is not None:
            return str(len(self.request['body']))
        else:
            return str(0)

    @property
    def content_type(self):
        try:
            return self.request['headers']['Content-Type']
        except KeyError:
            return None

    @property
    def url_scheme(self):
        if 'X-Forwarded-Proto' in self.request['headers']:
            return self.request['headers']['X-Forwarded-Proto']
        else:
            return 'http'

    @property
    def server_port(self):
        if self.url_scheme == 'https':
            return '443'
        else:
            return '80'

    @property
    def query_string(self):
        if self.request['queryStringParameters'] is None:
            return None
        else:
            return urlencode(self.request['queryStringParameters'])

    def __init__(self, request):
        self.request = request

        self.environ = {
            'REQUEST_METHOD': request['httpMethod'],
            'SCRIPT_NAME': '/{0}'.format(request['requestContext']['stage']),
            'PATH_INFO': request['path'],
            'QUERY_STRING':  self.query_string,
            'CONTENT_TYPE': self.content_type,
            'CONTENT_LENGTH': self.content_length,
            'SERVER_NAME':  request['headers']['Host'],
            'SERVER_PORT': self.server_port,
            'SERVER_PROTOCOL': 'HTTP/1.1',
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': self.url_scheme,
            'wsgi.input': self.body,
            'wsgi.errors': '',  # what should this be?
            'wsgi.multiprocess': False,
            'wsgi.multithread': False,
            'wsgi.run_once': False
        }

        headers = {'HTTP_{0}'.format(key.upper().replace('-', '_')): value
                   for key, value in request['headers'].iteritems()}

        self.environ.update(headers)
