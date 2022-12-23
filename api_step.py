import json

from BasicEndpoint import BasicEndpoint
from openai.api_resources.completion import Completion

from prompts.get_service import get_service_prompt
from prompts.get_endpoint import get_endpoint_prompt
from prompts.get_request import get_request_prompt

from models import ADA
from models import BABBAGE
from models import DAVINCI


def api_step(user_input, step, context_data):

    # Get the relevant service i.e. Twitter, Google Calendar, etc.
    service = get_service(user_input, step)

    print('Picking an endpoint for ' + service + '...')

    # Get the specification source and data for the specific service.
    # For example, for Twitter, spec_source = "openapi" and spec_data is the JSON data from specifications/openapi/twitter.json
    spec_source, spec_data = get_spec(service)

    # Get the endpoint and method needed for the API request.
    # For example, "GET /2/compliance/jobs"
    endpoint_method = get_endpoint_method(
        user_input, step, spec_source, spec_data)

    # Extract the endpoint and method from the above endpoint_method string.
    # For example, "/2/compliance/jobs"
    endpoint = endpoint_method.split(' ')[1].strip()
    # For example, "get"
    method = endpoint_method.split(' ')[0].strip().lower()

    print('Forming a ' + method + ' request...')

    # TODO
    # Get the request information, including URL, authorization, body, headers, etc.
    request = get_request(user_input, step, context_data,
                          endpoint, method, spec_source, spec_data)


def get_service(user_input, step):

    # ADA is a lightweight model, suitable for easy classification tasks.
    model = ADA
    # Service names will be no longer than 8 words.
    max_tokens = 8

    # Get every available service using services.json
    # e.g. ["twitter", "google calendar", etc.]
    available_services = get_available_services()

    # Get an AI prompt that asks for the service to use
    prompt = get_service_prompt(user_input, step, available_services)

    # Get completion
    completion = Completion.create(
        model=model,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=0
    )

    return completion.choices[0].text


def get_spec(service):

    # Load the service data.
    service_f = open('services.json')
    data = json.loads(service_f.read())

    service = service.lower()
    specification_source = '[Not Found]'

    # Get the specification source of the specified service.
    # For instance, Twitter uses OpenAPI Specification.
    # In this example, specification_source = "openapi".
    for service_data in data:
        if service_data['name'] == service:
            specification_source = service_data['specProvider']

    print('> Reading specification from ' + specification_source)

    # Get the file path of the specification json
    # The specifications are located at specifications/SOURCE/SERVICE.json.
    # For example, Twitter is located at specifications/openapi/twitter.json.
    spec_file_name = 'specifications/' + \
        specification_source + '/' + service + '.json'

    # Load the data from the specification
    spec_f = open(spec_file_name)
    data = json.loads(spec_f.read())

    spec_f.close()

    return specification_source, data


def get_endpoint_method(user_input, step, spec_source, spec_data):

    # Should the prompt that grabs the endpoint be printed to the console?
    # Set to True if you need to debug incorrect endpoints being grabbed.
    show_prompt = False

    # DAVINCI is a smart model capable of handling complex tasks.
    model = DAVINCI
    # An endpoint and method should be no longer than 32 words.
    max_tokens = 32

    # Get a list of endpoints for the service using the specification data.
    if spec_source == "openapi":
        basic_endpoints = get_basic_endpoints_openapi(spec_data)
    else:
        print('Error: Specification source not supported')

    print('> Choosing the best endpoint to use')

    basic_endpoints_str = ''

    # Create a string listing every endpoint, their methods and summaries.
    # This string will be fed into the prompt for the AI.
    for endpoint in basic_endpoints:
        endpoint_str = endpoint.path
        for method in endpoint.methods:
            endpoint_str = endpoint_str + '\n' + method
        basic_endpoints_str = basic_endpoints_str + '\n' + endpoint_str + '\n'

    # Get an AI prompt asking to choose an endpoint and method to use.
    prompt = get_endpoint_prompt(basic_endpoints_str, user_input, step)

    if show_prompt:
        print('> Prompt: \n\n' + prompt + '\n')

    # Get completion
    completion = Completion.create(
        model=model,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=0,
        stop='\n\n'
    )

    endpoint_result = completion.choices[0].text

    print('> Found endpoint: ' + endpoint_result)
    return endpoint_result


def get_request(user_input, step, context_data, endpoint, method, spec_source, spec_data):

    # DAVINCI is a smart model capable of handling complex tasks.
    model = DAVINCI
    # The request is complex, but may not be longer than 128 tokens (words and characters).
    max_tokens = 128

    # Get data slice from specification.
    endpoint_details = get_endpoint_details_openapi(
        spec_data, endpoint, method)

    # Get the AI prompt asking to form the request.
    prompt = get_request_prompt(
        user_input, step, context_data, endpoint_details)

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


def get_available_services():

    f = open('services.json')
    data = json.loads(f.read())

    available_services = []

    for item in data:
        available_services.append(item["name"])

    f.close()

    return available_services


def get_basic_endpoints_openapi(data):

    basic_endpoints = []

    for path, path_data in data['paths'].items():
        endpoint = BasicEndpoint()
        endpoint.path = path
        endpoint.methods = []
        for method, method_data in path_data.items():
            method_str = '(' + method.upper() + ') ' + method_data['summary']
            endpoint.methods.append(method_str)
        basic_endpoints.append(endpoint)

    return basic_endpoints


def get_endpoint_details_openapi(data, endpoint, method):

    return data['paths'][endpoint][method.lower()]
