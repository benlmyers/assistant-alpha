from openai.api_resources.completion import Completion
from models import DAVINCI
from models import log_cost

from prompts.subdivision import subdivision_prompt
from train.train_from import train_from


def subdivision(user_input, cost):

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

    log_cost(completion, cost)
    result = train_from(result, "subdivision", user_input=user_input)

    if ',' in result:
        steps = result.split(',')
    else:
        steps = [result]

    formatted_steps = [step.strip() for step in steps]

    return formatted_steps
