def get_parameters_prompt(**kwargs):

    if kwargs['pretrain'] and kwargs['pretrain'] == True:

        return f"""Task: {kwargs['user_input']}
Step: {kwargs['step']}

Context Data:

{kwargs['context_data']}

Parameters Specification:

{kwargs['parameters_data']}

Parameters Data Result:
{{\""""

    return f"""The following is a Step for a Task you (the Assistant) could complete in a single API call.

Task: {kwargs['user_input']}
Step: {kwargs['step']}

Here is some data that must be used in the call. This data may be from the user, or from the Assistant's context.

{kwargs['context_data']}

Here is the OpenAPI specification for the parameters you can use.

{kwargs['parameters_data']}

Here's an example of a valid result:

{{\"backfill_minutes\": 1, \"text\": \"Hello, world!\", \"tweet.fields\": \"created_at,geo,lang\"}}

Here are the parameters details (keys=parameter name, value=parameter value), in JSON format, you must use to complete the Step.
If a parameter is not required and not necessary (empty value, or DEFAULT), it should NOT be included. This should be a MINIMAL set of parameters:

{{\""""
