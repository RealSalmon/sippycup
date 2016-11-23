Sippy Cup
=========

Python Adaptor for Serving WSGI Applications with AWS Lambda and API Gateway
----------------------------------------------------------------------------

Sippy Cup is an *extremely* minimalistic `Python`_ adaptor that allows `WSGI`_
applications to be served using using `AWS API Gateway`_ and `AWS Lambda`_
proxy integration.

Sippy Cup converts the input format sent to an AWS Lambda function by API
Gateway into a `WSGI`_ environment that is used to run a the application.
The application's response is then converted to a format that can be understood
by API Gateway.

When the WSGI environment is created, some additional values from the event
sent to AWS Lambda from API Gateway are also added. See the demo app below
for how to access these.

- **apigateway:** True
- **apigateway.stageVariables:** API Gateway stage variables
- **apigateway.requestContext:** The event request context

Background
~~~~~~~~~~
`<https://ben.fogbutter.com/2016/11/09/introducing-sippy-cup.html>`_

Getting started
~~~~~~~~~~~~~~~

Installation
^^^^^^^^^^^^

Because you will eventually need to `create a deployment package`_, it
is highly recommended that you use a `virtualenv`_ when using Sippy Cup.

::

    pip install sippycup

Create a simple application
^^^^^^^^^^^^^^^^^^^^^^^^^^^

lambda\_function.py provides a demo application

.. code:: python

    # lambda_function.py

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
        # provides
        return jsonify({
            'requestContext': request.environ['apigateway.requestContext'],
            'stageVariables': request.environ['apigateway.stageVariables']
        })


    def lambda_handler(event, context):
        return sippycup(app, event, context)


    if __name__ == '__main__':
        app.run()



You will need to `create a deployment package`_ and use that to create a new
AWS Lambda function.

Finally, `set up an API Gateway proxy resource with the lambda proxy
integration`_. It is recommended to create resources on both ‘/’ and
‘/SOMEPREFIX’ unless you don’t need the ‘/’ route.

.. _Python: https://www.python.org/
.. _AWS API Gateway: https://aws.amazon.com/api-gateway/
.. _AWS Lambda: https://aws.amazon.com/lambda/
.. _WSGI: https://wsgi.readthedocs.io/en/latest/
.. _create a deployment package: https://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html
.. _virtualenv: https://virtualenv.pypa.io/en/stable/
.. _set up an API Gateway proxy resource with the lambda proxy integration: https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-set-up-simple-proxy.html#api-gateway-set-up-lambda-proxy-integration-on-proxy-resource
