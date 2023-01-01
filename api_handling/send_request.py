import requests
import re


def send_request(server, endpoint, method, path_params, query_params, body_data, auth, auth_loc):

    url = server + endpoint

    headers = {}

    # Match REGEX expressions for {param_name} in endpoint.
    path_params_keys = re.findall(r'{(.*?)}', endpoint)

    for keyword in path_params_keys:
        url = url.replace('{' + keyword + '}', path_params[keyword])
    if '{' in url or '}' in url:
        print('[x] Missing path parameter.')
        return

    if auth_loc == 'bearer':
        headers['Authorization'] = 'Bearer ' + auth

    if method.lower() == 'get':
        response = requests.get(url, query_params, headers=headers)
    elif method.lower() == 'post':
        response = requests.post(url, query_params, body_data, headers=headers)
    else:
        print('[x] Method not supported')

    return response
