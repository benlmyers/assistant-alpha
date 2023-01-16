from openai import Completion

from models import DAVINCI
from models import log_cost
from prompts.get_next_substep_context import get_next_substep_context_prompt
from train.train_from import train_from


def get_next_substep_context(user_input, step, substep, next_substep, response, cost):

    # Should the prompt that grabs the endpoint be printed to the console?
    # Set to True if you need to debug incorrect endpoints being grabbed.
    show_prompt = False

    # Should the resulting substep context be printed to the console?
    # Set to True if you need to debug context results.
    show_result = True

    # DAVINCI is a smart model capable of handling complex tasks.
    model = DAVINCI
    # Operations should be no longer than 128 tokens.
    max_tokens = 128

    # Get an AI prompt asking to choose an endpoint and method to use.
    prompt = get_next_substep_context_prompt(
        user_input, step, substep, next_substep, response)

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

    result = train_from(result, "get_next_substep_context",
                        user_input=user_input, step=step, next_substep=next_substep, response=response)

    if (show_result):
        print('> Found context: \n' + result)

    return result