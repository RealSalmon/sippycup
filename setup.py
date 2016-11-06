from distutils.core import setup

config = {
    'description': 'A nano framework for http requests proxied to AWS Lambda',
    'author': 'Ben Jones',
    'author_email': 'ben@fogbutter.com',
    'version': '0.1',
    'packages': ['sippycup'],
    'name': 'sippycup',
    'install_requires': ['Werkzeug']
}

setup(**config)