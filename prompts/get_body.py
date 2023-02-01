def get_body_prompt(user_input, step, context_data, body_data):

    return f"""The following is a Step for a Task you (the Assistant) could complete in a single API call.

Task: {user_input}
Step: {step}

Here is some data that must be used in the call. This data may be from the user, or from the Assistant's context.

{context_data}

Here is the OpenAPI specification for the requestBody.

{body_data}

Here is the requestBody details (fully expanded schemas), in JSON format, you must use to complete the Step.
If a schema is not required and not necessary (empty value), it should NOT be included.
The types and descriptions of properties should NOT be included.
Only the name and value of each included property should be listed.
If a property is not required and not necessary (empty value), it should NOT be included:

{{"
"""
