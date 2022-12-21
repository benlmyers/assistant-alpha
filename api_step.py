import json
import itertools as IT

from BasicEndpoint import BasicEndpoint
from openai.api_resources.completion import Completion

from prompts.get_service import get_service_prompt
from prompts.get_endpoint import get_endpoint_prompt

from models import ADA
from models import BABBAGE


def api_step(user_input, step, context_data):

    service = get_service(user_input, step)

    print('Picking an endpoint for ' + service + '...')

    endpoint = get_endpoint(user_input, step, service)


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


def get_endpoint(user_input, step, service):

    show_prompt = False

    model = BABBAGE
    max_tokens = 32

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

    if specification_source == "openapi":
        basic_endpoints = get_basic_endpoints_openapi(data)
    else:
        print('Error: Specification source not supported')

    spec_f.close()

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
            method_str = '(' + method.upper() + ') ' + \
                method_data['summary']
            endpoint.methods.append(method_str)
        basic_endpoints.append(endpoint)

    return basic_endpoints
