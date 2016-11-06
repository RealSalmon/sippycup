from werkzeug.routing import Map, Rule
from sippycup.response import Response


class SippyCup(object):

    def __init__(self):
        self.route_map = Map()
        self.request = None


    def run(self, request, context):
        self.response = Response()
        self.request = request
        try:

            adapter = self.route_map.bind('localhost')
            endpoint, values = adapter.match(
                path_info=self.request['path'],
                method=self.request['httpMethod']
            )

            self.response.body = endpoint(**values)

        except Exception as E:

            if hasattr(E, 'code'):
                self.response.statusCode = E.code
            else:
                self.response.statusCode = 500

            self.response.body = E.message

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
