from openai.api_resources.completion import Completion

from models import DAVINCI
from models import log_cost


def ai_step(user_input, step, context_data, cost):

    model = DAVINCI
    max_tokens = 256

    prompt = f"""
The following is a step for a Task you (the Assistant) could complete in a single AI text completion: this one.

Task: {user_input}
Step to Focus on: {step}
Relevant Context Data:
{context_data}

Correct completion data result:

"""

    # Get completion
    completion = Completion.create(
        model=model,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=0
    )

    log_cost(completion, cost)

    return completion.choices[0].text
