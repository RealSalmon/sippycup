class SippyCupApiGatewayResponse(object):

    @property
    def statusCode(self):
        return self._response.status_code

    @property
    def body(self):
        return self._response.get_data(True)

    @property
    def headers(self):
        return {key: value
                for key, value in self._response.headers.iteritems()}

    def __init__(self, response):
        self._response = response

    def __iter__(self):
        for key in ['statusCode', 'body', 'headers']:
            yield (key, getattr(self, key))
