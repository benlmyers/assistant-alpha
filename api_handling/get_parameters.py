import json

from openai import Completion

from models import DAVINCI
from prompts.get_parameters import get_parameters_prompt


def get_parameters(user_input, step, context_data, operation_data):

    # Should the prompt that grabs the endpoint be printed to the console?
    # Set to True if you need to debug incorrect endpoints being generated.
    show_prompt = False

    # DAVINCI is a smart model capable of handling complex tasks.
    model = DAVINCI
    # The parameters JSON data may not be longer than 256 tokens (words and characters).
    max_tokens = 512

    parameters_data = operation_data["parameters"]

    if parameters_data == []:
        return {}, {}

    # Get the AI prompt asking to form the request.
    prompt = get_parameters_prompt(
        user_input, step, context_data, parameters_data)

    if show_prompt:
        print('> Prompt: \n\n' + prompt + '\n')

    # Get completion
    completion = Completion.create(
        model=model,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=0
    )

    result = '{\"' + completion.choices[0].text

    print('> Using parameters: ' + result)

    # TODO: Parameters functionality changed. Ensure it works.
    result_data = json.loads(result)

    # {"Parameter name": "Parameter Value"}
    path_params = {}
    query_params = {}

    for parameter_data in operation_data['parameters']:
        name = parameter_data['name']
        loc = parameter_data['in']
        val = result_data[name]
        if loc == 'path':
            path_params[name] = val
        elif loc == 'query':
            query_params[name] = val
        else:
            # TODO: Support other parameter types.
            print('[!] Unsupported parameter type found')

    return path_params, query_params
