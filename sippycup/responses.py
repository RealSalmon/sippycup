import json
from datetime import date, datetime
from werkzeug.wrappers import Response


class SippyCupResponse(Response):

    @property
    def apigr(self):
        return {
            'statusCode': self.status_code,
            'body': self.get_data(True),
            'headers': {key: value for key, value in self.headers.iteritems()}
        }

    def __init__(self, response=None, status=None, headers=None,
                 mimetype=None, content_type=None, direct_passthrough=False):
        super(SippyCupResponse, self).__init__(
            response=response, status=status, headers=headers,
            mimetype=mimetype, content_type=content_type,
            direct_passthrough=direct_passthrough
        )
        self.headers['Content-Type'] = 'application/json'

    def redirect(self, url, code=302):
        self.status_code = code
        self.headers['Location'] = url

    def set_data(self, value):
        if self.headers['Content-Type'] == 'application/json':
            value = json.dumps(value, default=self.json_serializer)

        return super(SippyCupResponse, self).set_data(value)

    @staticmethod
    def json_serializer(obj):
        if type(obj) in [datetime, date]:
            return obj.isoformat()
        else:
            raise TypeError('{0}.{1} is not JSON serializable'.format(
                type(obj).__module__, type(obj).__name__
            ))
