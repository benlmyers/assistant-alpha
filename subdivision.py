from openai.api_resources.completion import Completion
from models import DAVINCI

from prompts.subdivision import subdivision_prompt


def subdivision(user_input):

    model = DAVINCI
    max_tokens = 512

    prompt = subdivision_prompt(user_input)

    # Get completion
    completion = Completion.create(
        model=model,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=0,
        stop='\n\n'
    )

    # Grab the steps from the completion.
    # The steps are comma-seperated, and in between the characters '[' and ']'.
    result = completion.choices[0]
    result = result.text

    if ',' in result:
        steps = result.split(',')
    else:
        steps = [result]

    formatted_steps = [step.strip() for step in steps]

    return formatted_steps
