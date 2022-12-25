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
    max_tokens = 256

    parameters_data = operation_data["parameters"]

    if parameters_data == []:
        return []

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

    result = '{\"name\": \"' + completion.choices[0].text

    print('> Using parameters:' + result)

    result_data = json.loads(result)

    return result_data
