from api_handling.security.oauth2 import oauth2
import json


def get_security(operation_data, spec_data, service):

    print('> Getting security schemes')

    security_schemes_data = spec_data['components']['securitySchemes']

    available_schemes_data = operation_data['security']
    available_schemes = []

    for available_scheme_data in available_schemes_data:
        available_schemes.append(list(available_scheme_data.keys())[0])

    i = 0
    for scheme in available_schemes:
        i += 1
        print('[' + str(i) + '] ' + scheme)

    choice = input('Choose an authentication method: ')

    use_scheme = available_schemes[int(choice) - 1]

    print('> Using ' + use_scheme)

    security_type = security_schemes_data[use_scheme]['type']

    if security_type == 'oauth2':
        access_code = oauth2(
            security_schemes_data[use_scheme], operation_data, service, use_scheme)
        return access_code, 'bearer'
    elif security_type == 'http':
        scheme = security_schemes_data[use_scheme]['scheme']
        if scheme == 'bearer':
            f = open('api_secrets.json')
            secrets = json.loads(f.read())
            f.close()
            return secrets[service]['bearer'], 'bearer'
        else:
            print('[x] Unsupported HTTP security scheme')
    else:
        print('[x] Unsupported security type')

    return '', 'error'
