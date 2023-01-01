def get_parameters_prompt(user_input, step, context_data, parameters_data):

    return f"""The following is a Step for a Task you (the Assistant) could complete in a single API call.

Task: {user_input}
Step: {step}

Here is some data that must be used in the call. This data may be from the user, or from the Assistant's context.

{context_data}

Here is the OpenAPI specification for the parameters you can use.

{parameters_data}

Here's an example of a valid result:

{{\"backfill_minutes\": 1, \"text\": \"Hello, world!\", \"tweet.fields\": \"created_at,geo,lang\"}}

Here are the parameters details (keys=parameter name, value=parameter value), in JSON format, you must use to complete the Step.
If a parameter is not required and not necessary (empty value, or DEFAULT), it should NOT be included. This should be a MINIMAL set of parameters:

{{\""""
