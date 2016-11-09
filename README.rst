Sippy Cup
=========

Python Serverless Nanoframework for AWS API Gateway and AWS Lambda
------------------------------------------------------------------

Sippy Cup is an *extremely* minimalistic `Python`_ framework to quickly
create serverless applications using `AWS API Gateway`_ and `AWS
Lambda`_.

Sippy Cup converts the input format sent to an AWS Lambda function by
API Gateway into a `WSGI`_ environment to provide a set of
`Werkzeug`_-based requestand response objects, converting the latter to
the return format expected by API Gateway.

It is intended to be similar in use to Python frameworks such as
`Flask`_ and `Chalice`_, although by design it has a significantly
smaller feature set.

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

    from sippycup import SippyCup

    app = SippyCup()


    @app.route('/hello/<string:name>', methods=['GET', 'POST'])
    @app.mimetype('text/plain')
    def hello_world(name='World'):
        return 'Hello, {0}!'.format(name)


    @app.route('/')
    def index():
        return app.request


    lambda_handler = app.run

You will the need to `create a deployment package`_ and use that to
create a new AWS Lambda function.

Finally, `set up an API Gateway proxy resource with the lambda proxy
integration`_. It is recommended to create resources on both ‘/’ and
‘/SOMEPREFIX’ unless you don’t need the ‘/’ route.

.. _Python: https://www.python.org/
.. _AWS API Gateway: https://aws.amazon.com/api-gateway/
.. _AWS Lambda: https://aws.amazon.com/lambda/
.. _WSGI: https://wsgi.readthedocs.io/en/latest/
.. _Werkzeug: http://werkzeug.pocoo.org/
.. _Flask: http://flask.pocoo.org/
.. _Chalice: https://github.com/awslabs/chalice
.. _create a deployment package: https://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html
.. _virtualenv: https://virtualenv.pypa.io/en/stable/
.. _set up an API Gateway proxy resource with the lambda proxy integration: https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-set-up-simple-proxy.html#api-gateway-set-up-lambda-proxy-integration-on-proxy-resource
