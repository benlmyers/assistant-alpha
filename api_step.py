import json

from openai.api_resources.completion import Completion

from models import ADA


def api_step(user_input, step, context_data):

    service = get_service(user_input, step)

    print('Picking an endpoint for ' + service + '...')


def get_service(user_input, step):

    model = ADA
    max_tokens = 128

    available_services = get_available_services()

    prompt = f"""
The following is a step for a Task you (the Assistant) could complete in a single API call.

Task: {user_input}
Step to Focus on: {step}

The following is a list of services available to use:
{available_services}

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


def get_endpoint(user_input, step, service):

    service_f = open('services.json')
    data = json.loads(service_f.read())

    specification_source = '[Not Found]'

    for service in data:
        if service['name'] == service:
            specification_source = service['specProvider']

    print('Reading specification from ' + specification_source)

    spec_f = open('specifications/' + specification_source + '/')
    data = json.lads(spec_f.read())

    

def get_available_services():

    f = open('services.json')
    data = json.loads(f.read())

    available_services = []

    for item in data:
        available_services.append(item["name"])

    f.close()

    return available_services
