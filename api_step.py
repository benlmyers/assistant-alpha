import json
from BasicEndpoint import BasicEndpoint
import itertools as IT

from openai.api_resources.completion import Completion

from models import BABBAGE
from models import DAVINCI


def api_step(user_input, step, context_data):

    service = get_service(user_input, step)

    print('Picking an endpoint for ' + service + '...')

    endpoint = get_endpoint(user_input, step, service)


def get_service(user_input, step):

    model = BABBAGE
    max_tokens = 128

    available_services = get_available_services()

    prompt = f"""The following is a list of services available to use:
{available_services}

Now the following is a step for a Task you (the Assistant) could complete in a single API call.

Task: Get a random Tweet
Step to Focus on: Fetch a random Tweet

The above service that should be used for this step is:
twitter

Task: {user_input}
Step to Focus on: {step}

The above service that should be used for this step is:
"""
    # Get completion
    completion = Completion.create(
        model=model,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=0
    )

    result = completion.choices[0].text

    if not result in available_services:
        print('[x] Service not found, using default service: twitter')
        result = 'twitter'

    return result


def get_endpoint(user_input, step, service):

    model = BABBAGE
    max_tokens = 128

    service_f = open('services.json')
    data = json.loads(service_f.read())

    service = service.lower()
    specification_source = '[Not Found]'

    for service_data in data:
        if service_data['name'] == service:
            specification_source = service_data['specProvider'].strip()

    print('> Reading specification from ' + specification_source)

    spec_f = open('specifications/' + specification_source +
                  '/' + service + '.json')
    data = json.loads(spec_f.read())

    basic_endpoints = get_basic_endpoints_openapi(data)
    spec_f.close()

    print('> Choosing the best endpoint to use')

    basic_endpoints_str = ''

    for endpoint in basic_endpoints:
        basic_endpoints_str = basic_endpoints_str + f"""

Path: {endpoint.path} ({endpoint.method})
Summary: {endpoint.summary}

        """

    prompt = f"""
The following is a step for a Task you (the Assistant) could complete in a single API call.

Task: {user_input}
Step to Focus on: {step}

And the following is a list of API endpoint paths, their methods and a quick summary about each of them:

{basic_endpoints_str}

And the following is one path + method, chosen from the above list, that should be used for this step.
Path:
"""

    completion = Completion.create(
        model=model,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=0
    )

    endpoint_result = completion.choices[0].text.strip()

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
        for method, method_data in path_data.items():
            endpoint = BasicEndpoint()
            endpoint.path = path
            endpoint.method = method
            endpoint.summary = path_data[method]['summary']
            print('>> Found endpoint: ' + endpoint.path +
                  ' (' + endpoint.method + ')')

    return basic_endpoints
