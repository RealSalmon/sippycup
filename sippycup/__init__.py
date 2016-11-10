from werkzeug.routing import Map, Rule, RequestRedirect, HTTPException
from sippycup.requests import SippyCupRequest, SippyCupApiGatewayRequest
from sippycup.responses import SippyCupResponse

class SippyCup(object):

    def __init__(self):
        self.route_map = Map()
        self.request = None
        self.response = None

    def dispatch_request(self, request):

        self.request = request
        self.response = SippyCupResponse()

        adapter = self.route_map.bind_to_environ(request.environ)
        result = None
        try:
            endpoint, values = adapter.match()
            result = endpoint(**values)
        except RequestRedirect as E:
            self.response.headers['Location'] = E.message
            self.response.status_code = 302
        except HTTPException as E:
            self.response.status_code = E.code
            self.response.headers['Content-Type'] = 'text/plain'
            result = E.description
        except Exception as E:
            # TODO: something useful...
            self.response.status_code = 500
            self.response.headers['Content-Type'] = 'text/plain'
            result = E.message

        self.response.set_data(result)

    def run(self, environ, start_response):
        if 'wsgi.version' in environ:
            # WSGI
            self.dispatch_request(SippyCupRequest(environ))
            return self.response(environ, start_response)
        else:
            # API Gateway
            self.dispatch_request(SippyCupApiGatewayRequest(environ))
            return self.response.apigr

    def route(self, route, defaults=None, methods=None):
        def wrapper(func):
            self.route_map.add(Rule(
                route,
                endpoint=func,
                defaults=defaults,
                methods=methods
            ))
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
