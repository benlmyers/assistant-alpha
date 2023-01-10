from openai.api_resources.completion import Completion

from prompts.ai_step import ai_step_prompt

from models import DAVINCI


def ai_step(user_input, step, context_data):

    model = DAVINCI
    max_tokens = 256

    prompt = ai_step_prompt(user_input, step, context_data)

    # Get completion
    completion = Completion.create(
        model=model,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=0
    )

    return completion.choices[0].text
