# Demo App for Sippy Cup

from flask import Flask, Response, request, jsonify, make_response
from sippycup import sippycup

app = Flask(__name__)

@app.route('/hello/', methods=['GET', 'POST'])
@app.route('/hello/<string:name>', methods=['GET', 'POST'])
def hello_world(name='World'):
    return Response('Hello, {0}!'.format(name), mimetype='text/plain')


@app.route('/')
def index():
    # return the additional WSGI environment variables that SippyCup
    # provides
    rc = request.environ['apigateway.requestContext']
    rc['accountId'] = 'xxxxxxxxxx'
    r = make_response(jsonify({
        'requestContext': rc,
        'stageVariables': request.environ['apigateway.stageVariables']
    }))
    r.set_cookie('cisfor', 'cookie')
    r.set_cookie('cookiestartswith', 'c')
    r.set_cookie('multiplecookies', 'is possible')
    return r


def lambda_handler(event, context):
    return sippycup(app, event, context)


if __name__ == '__main__':
    app.run()
