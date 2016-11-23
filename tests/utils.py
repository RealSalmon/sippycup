def get_apigr(request=None):
    return {
        'body': None,
        'resource': '/',
        'requestContext': {
            'resourceId': 'x1x2x3',
            'apiId': 'y1y2y3',
            'resourcePath': '/',
            'httpMethod': 'GET',
            'requestId': 'aeb82388-a4e8-11e6-a3ed-b5dcbcb63416',
            'accountId': 'z1z2z3',
            'identity': {
                'apiKey': None,
                'userArn': None,
                'cognitoAuthenticationType': None,
                'accessKey': None,
                'caller': None,
                'userAgent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                'user': None,
                'cognitoIdentityPoolId': None,
                'cognitoIdentityId': None,
                'cognitoAuthenticationProvider': None,
                'sourceIp': '127.0.0.1',
                'accountId': None
            },
            'stage': 'testing'
        },
        'queryStringParameters': None,
        'httpMethod': 'GET',
        'pathParameters': None,
        'headers': {
            'Via': '1.1 a536f7c9dbedc2b462a158901fcd8254.cloudfront.net (CloudFront)',
            'Accept-Language': 'en-US,en;q=0.8',
            'CloudFront-Is-Desktop-Viewer': 'true',
            'CloudFront-Is-SmartTV-Viewer': 'false',
            'CloudFront-Is-Mobile-Viewer': 'false',
            'X-Forwarded-For': '104.56.41.168, 54.240.159.59',
            'CloudFront-Viewer-Country': 'US',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Upgrade-Insecure-Requests': '1',
            'X-Forwarded-Port': '443',
            'Host': 'testing.fogbutter.com',
            'X-Forwarded-Proto': 'https',
            'X-Amz-Cf-Id': '03xj4hdvvnK7SX_cVWC2YOLVzl-H-UOX1FfBFcopVr5RYogDGbD6sw==',
            'CloudFront-Is-Tablet-Viewer': 'false',
            'Cache-Control': 'max-age=0',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
            'CloudFront-Forwarded-Proto': 'https',
            'Accept-Encoding': 'gzip, deflate, sdch, br'
        },
        'stageVariables': {
            "ben": "was-here",
            "so_was": "red"
        },
        'path': '/'
    }

