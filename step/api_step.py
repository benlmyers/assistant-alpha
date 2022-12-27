from openai.api_resources.completion import Completion

from api_handling.get_operation import get_operation
from api_handling.get_parameters import get_parameters
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

    # Get the opeartion needed for the API request.
    # For example, "GET /2/compliance/jobs"
    operation = get_operation(
        user_input, step, spec_source, spec_data)

    # Extract the endpoint and method from the above operation string.
    # For example, "/2/compliance/jobs"
    endpoint = operation.split(' ')[1].strip()
    # For example, "get"
    method = operation.split(' ')[0].strip().lower()

    operation_data = spec_data['paths'][endpoint][method.lower()]

    print('Getting parameters...')

    # Get the parameters data for the request.
    parameters_data = get_parameters(
        user_input, step, context_data, operation_data)

    print('Getting authorization...')

    access_code = get_security(operation_data, spec_data, service)
