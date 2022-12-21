def get_request_prompt(user_input, step, context_data, endpoint_details):

    return f"""The following is a Step for a Task you (the Assistant) could complete in a single API call

Task: {user_input}
Step: {step}

Here is some data that must be used in the call. This data may be from the user, or from the Assistant's context.

{context_data}

Here is the OpenAPI specification for the endpoint and method you must use.

{endpoint_details}

Here are the request details (API call, headers, body, etc.) you must use to complete the Step:
"""
