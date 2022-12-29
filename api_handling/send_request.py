def send_request(server, endpoint, method, parameters_data, operation_data, body_data, auth, auth_loc):

    url = server + endpoint

    path_parameters = {}

    for parameter_data in parameters_data:

        if parameter_data['in'] == 'path':
            path_parameters[parameter_data['name']] = parameter