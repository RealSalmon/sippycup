# Demo App for Sippy Cup

from flask import Flask, Response, request, jsonify
from sippycup import sippycup

app = Flask(__name__)

@app.route('/hello/', methods=['GET', 'POST'])
@app.route('/hello/<string:name>', methods=['GET', 'POST'])
def hello_world(name='World'):
    return Response('Hello, {0}!'.format(name), mimetype='text/plain')


@app.route('/')
def index():
    # return the additional WSGI environment variables that SippyCup
    # provided
    return jsonify({
        'requestContext': request.environ['apigateway.requestContext'],
        'stageVariables': request.environ['apigateway.stageVariables']
    })


def lambda_handler(event, context):
    return sippycup(app, event, context)


if __name__ == '__main__':
    app.run()
