def get_endpoint_method(raw_operation):

    # Extract the endpoint and method from the above operation string.
    # For example, "/2/compliance/jobs"
    endpoint = raw_operation.split(' ')[1].strip()
    # For example, "get"
    method = raw_operation.split(' ')[0].strip().lower()

    return endpoint, method
