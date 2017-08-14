from setuptools import setup

with open('README.rst') as readme_file:
    README = readme_file.read()

config = {
    'description': 'An adaptor for serving WSGI applications using AWS Lambda and API Gateway',
    'long_description': README,
    'url': 'https://bitbucket.org/realsalmon/sippycup',
    'author': 'Ben Jones',
    'author_email': 'ben@fogbutter.com',
    'version': '0.5.0',
    'packages': ['sippycup'],
    'name': 'sippycup',
    'install_requires': [],
    'license': 'MIT',
    'classifiers': [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development'
    ],
    'keywords': 'aws lambda api serverless wsgi',
    'extras_require': {
        'test': ['tox', 'pytest', 'pytest-cov', 'flask'],
    },

}

setup(**config)
