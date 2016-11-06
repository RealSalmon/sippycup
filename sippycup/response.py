import json


class Response(object):

    def __init__(self):
        self.headers = {'Content-Type': 'application/json'}
        self.body = None
        self.statusCode = 200

    def redirect(self, url, code=302):
        self.headers['Location'] = url
        self.body = None
        self.statusCode = code

    def send(self):

        if self.headers['Content-Type'] == 'application/json':
            body = json.dumps(self.body)
        else:
            body = self.body

        return {
            'headers': self.headers,
            'statusCode': self.statusCode,
            'body': body
        }
