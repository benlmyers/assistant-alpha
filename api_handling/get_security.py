from api_handling.security.oauth2 import oauth2
import json


def get_security(operation_data, spec_data, service):

    print('> Getting security scheme')

    security_schemes_data = spec_data['components']['securitySchemes']

    security_schemes_keys = security_schemes_data.keys()

    security_schemes = []

    for key in security_schemes_keys:
        security_schemes_data[key]['name'] = key
        security_schemes.append(security_schemes_data[key])

    for scheme in security_schemes:
        if scheme['type'] == 'oauth2':
            access_code = oauth2(scheme, operation_data, service)
            return access_code, 'bearer'

    return '', 'error'
