from werkzeug.routing import Map, Rule, RequestRedirect
from sippycup.response import Response


class SippyCup(object):

    @property
    def _script_name(self):
        try:
            return '/{0}/'.format(self.request['requestContext']['stage'])
        except KeyError:
            return None

    @property
    def _host(self):
        try:
            return self.request['headers']['Host']
        except KeyError:
            return 'localhost'

    def __init__(self):
        self.route_map = Map()
        self.request = None
        self.response = None

    def run(self, request, context):
        self.response = Response()
        self.request = request
        try:

            adapter = self.route_map.bind(
                self._host,
                script_name=self._script_name,
                url_scheme='https'
            )

            endpoint, values = adapter.match(
                path_info=self.request['path'],
                method=self.request['httpMethod']
            )

            self.response.body = endpoint(**values)
        except RequestRedirect as E:
            self.response.statusCode = 302
            self.response.headers['Location'] = E.message
        except Exception as E:

            if hasattr(E, 'code'):
                self.response.statusCode = E.code
            else:
                self.response.statusCode = 500

            self.response.body = str(E)

        return self.response.send()

    def route(self, route, defaults=None, methods=None):
        def wrapper(func):
            self.route_map.add(Rule(route, endpoint=func, defaults=defaults, methods=methods))
            return func

        return wrapper

    def mimetype(self, mimetype):

        # Initial level is required to accept argument

        def wrapper(func):
            # Now we are in the real decorator, which is called at the time
            # of decoration

            def wrapper2(*args, **kwargs):
                # This is the wrapper, which is used to to replace the original
                # fx and called at that time
                x = func(*args, **kwargs)
                self.response.headers['Content-Type'] = mimetype
                return x

            return wrapper2

        return wrapper
