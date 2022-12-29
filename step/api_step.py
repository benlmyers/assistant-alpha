from openai.api_resources.completion import Completion

from api_handling.get_operation import get_operation
from api_handling.get_parameters import get_parameters
from api_handling.get_body import get_body
from api_handling.get_service import get_service
from api_handling.get_spec import get_spec
from api_handling.get_security import get_security
from models import DAVINCI
from prompts.get_request import get_request_prompt


def api_step(user_input, step, context_data):

    # Get the relevant service i.e. Twitter, Google Calendar, etc.
    service = get_service(user_input, step)

    print('Picking an endpoint for ' + service + '...')

    # Get the specification source and data for the specific service.
    # For example, for Twitter, spec_source = "openapi" and spec_data is the JSON data from specifications/openapi/twitter.json
    spec_source, spec_data = get_spec(service)

    # Get the operations needed for the API request.
    # For example, "GET /2/compliance/jobs (goal)"
    raw_operations = get_operations(
        user_input, step, spec_source, spec_data)

    raw_operations = raw_operations.split('\n')

    for raw_operation in raw_operations:
        # Extract the endpoint and method from the above operation string.
        # For example, "/2/compliance/jobs"
        endpoint = raw_operation.split(' ')[1].strip()
        # For example, "get"
        method = raw_operation.split(' ')[0].strip().lower()
        # The mini-summary to use with this specific operation.
        substep = raw_operation.split(' ')[2].strip()

        # Step description (substep description)
        detailed_step = step + ' ' + substep

        operation_data = spec_data['paths'][endpoint][method.lower()]

        print('Getting parameters...')

        # Get the parameters data for the request.
        parameters_data = get_parameters(
            user_input, detailed_step, context_data, operation_data)

        if (method == 'post'):
            print('Getting request body...')

            # Get the parameters data for the request.
            body_data = get_body(
                user_input, detailed_step, context_data, operation_data)

        print('Getting authorization...')

        authorization, auth_location = get_security(
            operation_data, spec_data, service)
