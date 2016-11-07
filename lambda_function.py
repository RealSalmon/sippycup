# Sippy Cup demo app

from sippycup import SippyCup

app = SippyCup()


@app.route('/hello/<string:name>', methods=['GET', 'POST'])
@app.route('/hello/')
@app.mimetype('text/plain')
def hello_world(name='World'):
    return 'Hello, {0}!'.format(name)


@app.route('/data/', methods=['POST'])
def data():
    return app.request.json


@app.route('/')
@app.route('/deeper/path/')
def index():
    r = app.request.apigr
    if r is not None:
        for key in ['accountId', 'apiId', 'resourceId']:
            r['requestContext'][key] = 'xxxxx (removed...)'
        return r
    else:
        app.response.headers['Content-Type'] = 'text/plain'
        return "Not in an API Gateway . . ."


lambda_handler = app.run

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple(
        '127.0.0.1', 5000, lambda_handler, use_debugger=True, use_reloader=True
    )
