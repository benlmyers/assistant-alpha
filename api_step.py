import json

from openai.api_resources.completion import Completion

from models import ADA


def api_step(user_input, step, context_data):

    service = service(user_input, step)


def service(user_input, step):

    model = ADA
    max_tokens = 128

    prompt = f"""
The following is a step for a Task you (the Assistant) could complete in a single API call.

Task: {user_input}
Step to Focus on: {step}

The following is a list of services available to use:
Twitter, Gmail

The service that should be used for this step is:
"""

    # Get completion
    completion = Completion.create(
        model=model,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=0
    )

    return completion.choices[0].text
