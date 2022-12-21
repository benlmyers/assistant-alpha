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

    service = get_service(user_input, step)

    print('Picking an endpoint for ' + service + '...')

    spec_source, spec_data = get_spec(service)

    endpoint_method = get_endpoint_method(
        user_input, step, spec_source, spec_data)

    endpoint = endpoint_method.split(' ')[1].strip()
    method = endpoint_method.split(' ')[0].strip().lower()

    print('Forming a ' + method + ' request...')

    request = get_request(user_input, step, context_data,
                          endpoint, method, spec_source, spec_data)


def get_service(user_input, step):

    model = ADA
    max_tokens = 128

    available_services = get_available_services()

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

    service_f = open('services.json')
    data = json.loads(service_f.read())

    service = service.lower()
    specification_source = '[Not Found]'

    for service_data in data:
        if service_data['name'] == service:
            specification_source = service_data['specProvider']

    print('> Reading specification from ' + specification_source)

    spec_file_name = 'specifications/' + \
        specification_source + '/' + service + '.json'

    spec_f = open(spec_file_name)
    data = json.loads(spec_f.read())

    spec_f.close()

    return specification_source, data


def get_endpoint_method(user_input, step, spec_source, spec_data):

    show_prompt = False

    model = DAVINCI
    max_tokens = 32

    if spec_source == "openapi":
        basic_endpoints = get_basic_endpoints_openapi(spec_data)
    else:
        print('Error: Specification source not supported')

    print('> Choosing the best endpoint to use')

    basic_endpoints_str = ''

    for endpoint in basic_endpoints:
        endpoint_str = endpoint.path
        for method in endpoint.methods:
            endpoint_str = endpoint_str + '\n' + method
        basic_endpoints_str = basic_endpoints_str + '\n' + endpoint_str + '\n'

    prompt = get_endpoint_prompt(basic_endpoints_str, user_input, step)

    if show_prompt:
        print('> Prompt: \n\n' + prompt + '\n')

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

    model = DAVINCI
    max_tokens = 128

    # Get data slice from specification
    endpoint_details = get_endpoint_details_openapi(
        spec_data, endpoint, method)

    prompt = get_request_prompt(
        user_input, step, context_data, endpoint_details)

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
