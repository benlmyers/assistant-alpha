def send_request(server, endpoint, method, path_params, query_params, body_data, auth, auth_loc):

    url = server + endpoint

    # TODO: Match expressions within { }""
    keywords = []

    for keyword in keywords:
        url = url.replace('{' + keyword + '}', path_params[keyword])

    # TODO: Implement for each auth location.
    if auth_loc == 'bearer':
        # Header - Authorization: Bearer {value}
        pass
    elif auth_loc == 'authorizationCode':
        # Header - Authorization Bearar {value}
        pass
    elif auth_loc == 'apiKey':
        # Could be anywhere. Need to reread openapi spec
        pass

    # TODO: Form and send the request.

    # TODO: Get the response data.
    return
