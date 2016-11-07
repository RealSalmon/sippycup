import json
from werkzeug.wrappers import Request
from werkzeug.utils import cached_property
from .wsgienviron import WsgiEnviron


class SippyCupRequest(Request):

    _apigr = None

    @property
    def apigr(self):
        """The raw request/event from API Gateway"""
        return self._apigr

    @cached_property
    def json(self):
        if self.headers.get('content-type') == 'application/json':
            return json.loads(self.data)


class SippyCupApiGatewayRequest(SippyCupRequest):
    def __init__(self, event):
        self._apigr = event
        environ = WsgiEnviron(event).environ
        super(SippyCupApiGatewayRequest, self).__init__(environ)
