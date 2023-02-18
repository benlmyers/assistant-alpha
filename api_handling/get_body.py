import json

from openai import Completion

from models import DAVINCI
from models import log_cost
from prompts.get_body import get_body_prompt
from train.train_from import train_from
from util.get_endpoint_method import get_endpoint_method
from api_handling.get_spec import get_spec


def get_body(user_input, step, context_data, cost, service, operation):

    # Should the prompt that grabs the endpoint be printed to the console?
    # Set to True if you need to debug incorrect endpoints being generated.
    show_prompt = True

    # DAVINCI is a smart model capable of handling complex tasks.
    model = DAVINCI
    # The parameters JSON data may not be longer than 256 tokens (words and characters).
    max_tokens = 256

    body_data = get_body_spec_data(service, operation)

    if body_data == []:
        return []

    # Get the AI prompt asking to form the request.
    prompt = get_body_prompt(
        user_input=user_input, step=step, context_data=context_data, body_data=body_data)

    if show_prompt:
        print('> Prompt: \n\n' + prompt + '\n')

    # Get completion
    completion = Completion.create(
        model=model,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=0
    )

    log_cost(completion, cost)

    result = '{"' + completion.choices[0].text

    result = train_from(result, "get_body",
                        user_input=user_input, step=step, context_data=context_data, service=service, operation=operation)

    print('> Using body: ' + result)

    result_data = json.loads(result)

    return result_data


def get_body_spec_data(service, operation):

    spec_source, spec_data = get_spec(service)

    endpoint, method = get_endpoint_method(operation)

    operation_data = spec_data['paths'][endpoint][method.lower()]

    return operation_data['requestBody']
