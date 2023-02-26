def get_body_prompt(**kwargs):

    if 'pretrain' in kwargs and kwargs['pretrain'] == True:

        return f"""Task: {kwargs['user_input']}
Step: {kwargs['step']}

Context Data:

{kwargs['context_data']}

Request Body Specification:

{kwargs['body_data']}
    
Request Body Data Result:

{{"
"""

    return f"""The following is a Step for a Task you (the Assistant) could complete in a single API call.

Task: {kwargs['user_input']}
Step: {kwargs['step']}

Here is some data that must be used in the call. This data may be from the user, or from the Assistant's context.

{kwargs['context_data']}

Here is the OpenAPI specification for the requestBody.

{kwargs['body_data']}
    
    Here is the requestBody details (fully expanded schemas), in JSON format, you must use to complete the Step.
If a schema is not required and not necessary (empty value), it should NOT be included.
The types and descriptions of properties should NOT be included.
Only the name and value of each included property should be listed.
If a property is not required and not necessary (empty value), it should NOT be included:

{{"
"""
