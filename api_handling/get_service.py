import json

from openai import Completion

from models import CURIE
from prompts.get_service import get_service_prompt
from train.train_from import train_from
from models import log_cost


def get_service(user_input, step, cost):

    show_prompt = False

    # ADA is a lightweight model, suitable for easy classification tasks.
    model = CURIE
    # Service names will be no longer than 8 words.
    max_tokens = 8

    # Get every available service using services.json
    # e.g. ["twitter", "google calendar", etc.]
    available_services = get_available_services()

    available_services = str(available_services).replace("'", '')

    # Get an AI prompt that asks for the service to use
    prompt = get_service_prompt(
        user_input=user_input, step=step, available_services=available_services)

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

    result = completion.choices[0].text.strip()

    result = train_from(result, "get_service",
                        user_input=user_input, step=step)

    return result


def get_available_services():

    f = open('services.json')
    data = json.loads(f.read())

    available_services = []

    for item in data:
        available_services.append(item["name"])

    f.close()

    return available_services
