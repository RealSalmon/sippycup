import itertools
from sys import stderr, stdout
try:
    from urllib import urlencode
    from StringIO import StringIO
except ImportError:
    from urllib.parse import urlencode
    from io import StringIO


def sippycup(app, event, context=None):
    response = SippyCupResponse()
    result = app(WsgiEnviron(event).environ, response)
    return response.apigr(result)


class SippyCupResponse:

    def apigr(self, body=''):

        # The response format states that headers must be a dictionary, which
        # presents a problem when multiple Set-Cookie headers are returned by
        # the application (only the last cookie set gets put into the response)
        #
        # Browser's seem not to care about the case of the header name, and
        # API Gateway does not alter the header names.
        #
        # As such, setting multiple cookies in the response seems to be
        # possible by simply using a different case permutations of 'Set-Cookie'
        #
        # Generation of case permutations comes from ephemient on StackOverflow
        # https://stackoverflow.com/questions/11144389/find-all-upper-lower-and-mixed-case-combinations-of-a-string

        headers = {h[0]: h[1] for h in self.headers
                   if h[0].lower() != 'set-cookie'}

        headers.update(zip(
            map(
                ''.join,
                itertools.product(
                    *zip('set-cookie'.upper(), 'set-cookie'.lower()))
            ),
            [h[1] for h in self.headers if h[0].lower() == 'set-cookie']
        ))

        return {
            'statusCode': int(self.status.split()[0]),
            'body': ''.join(
                [self.body.getvalue()] +
                [x.decode(stdout.encoding or 'UTF8') for x in body]
            ),
            'headers': headers
        }

    def __init__(self):
        self.status = '200 OK'
        self.headers = []
        self.body = StringIO()

    def __call__(self, status, headers, exc_info=None):
        self.status = str(status)
        self.headers = list(headers)
        return self.body.write


class WsgiEnviron(object):

    # https://www.python.org/dev/peps/pep-0333/

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
        header = [val for key, val in self.request['headers'].items()
                  if key.lower() == 'content-type']
        try:
            return header[0]
        except IndexError:
            return None

    @property
    def query_string(self):
        if self.request['queryStringParameters'] is None:
            return ''
        else:
            return urlencode(self.request['queryStringParameters'])

    @property
    def script_name(self):
        if 'SIPPYCUP_SCRIPT_NAME_BASE' in self.request['stageVariables']:
            base = self.request['stageVariables']['SIPPYCUP_SCRIPT_NAME_BASE'].rstrip('/')
        else:
            base = ''.join(['/', self.request['requestContext']['stage']])

        return '/'.join([base, self.resource_path_base.lstrip('/')]).rstrip('/')

    @property
    def resource_path_base(self):
        end = self.request['requestContext']['resourcePath'].rfind('/{proxy+}')
        if end == -1:
            end = None
        return self.request['requestContext']['resourcePath'][0:end].rstrip('/')

    @property
    def path_info(self):
        return self.request['path'].replace(self.resource_path_base, '', 1)

    def __init__(self, request):

        if request['stageVariables'] is None:
            request['stageVariables'] = {}

        self.request = request

        self.environ = {
            'REQUEST_METHOD': request['httpMethod'],
            'SCRIPT_NAME': self.script_name,
            'PATH_INFO': self.path_info,
            'QUERY_STRING':  self.query_string,
            'CONTENT_TYPE': self.content_type,
            'CONTENT_LENGTH': self.content_length,
            'SERVER_NAME':  request['headers']['Host'],
            'SERVER_PORT': '443',
            'SERVER_PROTOCOL': 'HTTP/1.1',
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': 'https',
            'wsgi.input': self.body,
            'wsgi.errors': stderr,
            'wsgi.multiprocess': False,
            'wsgi.multithread': False,
            'wsgi.run_once': False,
            'apigateway.stageVariables': request['stageVariables'],
            'apigateway.requestContext': request['requestContext'],
            'apigateway': True
        }

        headers = {'HTTP_{0}'.format(key.upper().replace('-', '_')): value
                   for key, value in request['headers'].items()}

        self.environ.update(headers)
