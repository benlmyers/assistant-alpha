from openai import Completion

from Endpoint import Endpoint
from models import CURIE
from models import log_cost
from prompts.get_operations import get_operations_prompt
from train.train_from import train_from


def get_operations(user_input, step, all_steps, spec_source, spec_data, service, cost):

    # Should the prompt that grabs the endpoint be printed to the console?
    # Set to True if you need to debug incorrect endpoints being grabbed.
    show_prompt = False

    # CURIE is a smart model capable of handling moderate tasks.
    model = CURIE
    # Operations should be no longer than 128 tokens.
    max_tokens = 128

    # Get a list of endpoints for the service using the specification data.
    if spec_source == "openapi":
        endpoints = get_endpoints_openapi(spec_data)
    else:
        print('[x] Specification source not supported')

    endpoints_str = get_endpoints_str(endpoints)

    print('> Choosing the best endpoint to use')

    # Get an AI prompt asking to choose an endpoint and method to use.
    prompt = get_operations_prompt(
        endpoints_str=endpoints_str, user_input=user_input, step=step, all_steps=all_steps)

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

    log_cost(completion, cost)

    result = completion.choices[0].text

    result = train_from(result, "get_operations",
                        user_input=user_input, step=step, service=service)

    operations_result = result.strip()

    print('> Found operations: \n' + operations_result)
    return operations_result


def get_endpoints_openapi(data):

    endpoints = []

    for path, path_data in data['paths'].items():
        endpoint = Endpoint()
        endpoint.path = path
        endpoint.operations = []
        for method, method_data in path_data.items():
            if not ('summary' in method_data or 'description' in method_data):
                continue
            if 'summary' in method_data:
                method_str = '(' + method.upper() + ') ' + \
                    method_data['summary']
            else:
                method_str = '(' + method.upper() + ') ' + \
                    method_data['description']
            endpoint.operations.append(method_str)
        endpoints.append(endpoint)

    return endpoints


def get_endpoints_str(endpoints):

    endpoints_str = ''

    # Create a string listing every endpoint, their methods and summaries.
    # This string will be fed into the prompt for the AI.
    for endpoint in endpoints:
        for operation in endpoint.operations:
            endpoints_str = endpoints_str + '\n' + operation

    return endpoints_str
