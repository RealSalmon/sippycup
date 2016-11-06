# Sippy Cup demo app

from sippycup import SippyCup

app = SippyCup()


@app.route('/hello/<string:name>', methods=['GET', 'POST'])
@app.route('/hello/')
@app.mimetype('text/plain')
def hello_world(name='World'):
    return 'Hello, {0}!'.format(name)


@app.route('/')
def index():
    r = app.request
    for key in ['accountId', 'apiId', 'resourceId']:
        r['requestContext'][key] = 'xxxxx (removed...)'
    return r


lambda_handler = app.run
