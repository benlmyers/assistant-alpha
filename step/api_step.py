from openai.api_resources.completion import Completion

from api_handling.get_operation import get_operation
from api_handling.get_parameters import get_parameters
from api_handling.get_service import get_service
from api_handling.get_spec import get_spec
from api_handling.get_url import get_url
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

    print('Forming a ' + method + ' request...')

    # Get the parameters for the request.
    path_parameters, query_parameters, header_parameters = get_parameters()


def get_request(user_input, step, context_data, endpoint, method, spec_source, spec_data):

    # Should the prompt that grabs the endpoint be printed to the console?
    # Set to True if you need to debug incorrect endpoints being generated.
    show_prompt = True

    # DAVINCI is a smart model capable of handling complex tasks.
    model = DAVINCI
    # The request is complex, but may not be longer than 128 tokens (words and characters).
    max_tokens = 128

    # Get data slice from specification.
    if spec_source == "openapi":
        endpoint_details = get_endpoint_details_openapi(
            spec_data, endpoint, method)
    else:
        print('Error: Specification source not supported')

    # Get the AI prompt asking to form the request.
    prompt = get_request_prompt(
        user_input, step, context_data, endpoint_details)

    if show_prompt:
        print('> Prompt: \n\n' + prompt + '\n')

    # Get completion
    completion = Completion.create(
        model=model,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=0
    )

    result = completion.choices[0].text

    print('> Result:\n' + result)
    return result


def get_endpoint_details_openapi(data, endpoint, method):

    return data['paths'][endpoint][method.lower()]
