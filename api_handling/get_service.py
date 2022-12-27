import json

from openai import Completion

from models import ADA
from prompts.get_service import get_service_prompt


def get_service(user_input, step):

    # ADA is a lightweight model, suitable for easy classification tasks.
    model = ADA
    # Service names will be no longer than 8 words.
    max_tokens = 8

    # Get every available service using services.json
    # e.g. ["twitter", "google calendar", etc.]
    available_services = get_available_services()

    # Get an AI prompt that asks for the service to use
    prompt = get_service_prompt(user_input, step, available_services)

    # Get completion
    completion = Completion.create(
        model=model,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=0
    )

    return completion.choices[0].text


def get_available_services():

    f = open('services.json')
    data = json.loads(f.read())

    available_services = []

    for item in data:
        available_services.append(item["name"])

    f.close()

    return available_services