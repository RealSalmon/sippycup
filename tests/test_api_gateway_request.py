import json
from sippycup.requests import SippyCupApiGatewayRequest
from utils import get_apigr


def test_apigr():
    event = get_apigr()
    request = SippyCupApiGatewayRequest(event)
    assert request.apigr == event


def test_query_args():
    event = get_apigr()
    event['queryStringParameters'] = {
        'param1': 'something',
        'param2': 'something else'
    }
    request = SippyCupApiGatewayRequest(event)
    assert request.args['param1'] == 'something'
    assert request.args['param2'] == 'something else'


def test_host():
    event = get_apigr()
    request = SippyCupApiGatewayRequest(event)
    assert request.host == event['headers']['Host']


def test_cookies():
    event = get_apigr()
    event['headers']['Cookie'] = 'C is for cookie=That good enough for me; Cookie cookie cookie=start with c'
    request = SippyCupApiGatewayRequest(event)
    assert request.cookies['C is for cookie'] == 'That good enough for me'
    assert request.cookies['Cookie cookie cookie'] == 'start with c'


def test_json():
    event = get_apigr()
    event['body']= json.dumps({'ohai': 'there'})
    event['headers']['Content-Type'] = 'application/json'
    request = SippyCupApiGatewayRequest(event)
    assert 'ohai' in request.json
    assert request.json['ohai'] == 'there'


def test_form():
    event = get_apigr()
    event['body'] = "ohai=there"
    event['headers']['Content-Type'] = 'application/x-www-form-urlencoded'
    request = SippyCupApiGatewayRequest(event)
    assert 'ohai' in request.form
    assert request.form['ohai'] == 'there'
