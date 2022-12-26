import json

from api_handling.security.oauth2_flows.authorization_code import authorization_code


def oauth2(scheme_data, operation_data, service):

    print('> Using OAuth 2.0')

    flows_data = scheme_data['flows']
    scheme_name = scheme_data['name']

    print('> Getting consumer credentials')

    consumer_key, consumer_secret = get_consumer_credentials(service)

    print('> Getting scopes')

    for security_method in operation_data['security']:
        if scheme_name in security_method:
            scopes = security_method[scheme_name]

    print('> Using scopes: ' + ', '.join(scopes))

    # https://developer-stg.byu.edu/docs/consume-api/use-api/oauth-20/oauth-20-python-sample-code

    if flows_data['authorizationCode']:
        access_code = authorization_code(
            flows_data['authorizationCode'], consumer_key, consumer_secret, scopes)

    print('> Found access code: ' + access_code)

    return access_code


def get_consumer_credentials(service):

    f = open('api_secrets.json')

    secrets = json.loads(f.read())

    f.close()

    consumer_key = secrets[service]['consumerKey']
    consumer_secret = secrets[service]['consumerSecret']

    return consumer_key, consumer_secret
