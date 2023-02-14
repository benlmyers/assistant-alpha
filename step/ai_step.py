from openai.api_resources.completion import Completion

from prompts.ai_step import ai_step_prompt

from models import DAVINCI
from models import log_cost


def ai_step(user_input, step, context_data, cost):

    model = DAVINCI
    max_tokens = 256

    prompt = ai_step_prompt(user_input=user_input,
                            step=step, context_data=context_data)

    # Get completion
    completion = Completion.create(
        model=model,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=0
    )

    log_cost(completion, cost)

    return completion.choices[0].text
