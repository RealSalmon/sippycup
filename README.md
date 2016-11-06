# Sippy Cup

## A nano framework for http requests proxied to AWS Lambda

[Set Up a Proxy Resource with the Lambda Proxy Integration](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-set-up-simple-proxy.html#api-gateway-set-up-lambda-proxy-integration-on-proxy-resource)

```python
# lambda_function

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

```
