import json
from prompts.subdivision import subdivision_prompt


def generate_training_data():

    execute_processes = [
        'subdivision',
        'io',
        'get_service',
        'get_operations',
        'get_parameters',
        'get_body',
        'get_next_step_context',
        'get_next_substep_context'
    ]

    f = open('training_elements.json')
    data = json.loads(f.read())
    f.close()

    for process in execute_processes:

        training_pairs = []

        for training_element in data[process]:

            completion = training_element['result']

            del training_element['result']

            args = training_element

            prompt = ''

            if process == 'subdivision':
                prompt = subdivision_prompt(args)
            # ...
