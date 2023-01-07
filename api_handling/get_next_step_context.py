from openai import Completion

from models import DAVINCI
from prompts.get_next_step_context import get_next_step_context_prompt

def get_next_step_context(user_input, step, response):

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
    prompt = get_next_step_context_prompt(user_input, step, response)

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

    substep_context_result = completion.choices[0].text

    if(show_result):
        print('> Found context: \n' + substep_context_result)

    return substep_context_result