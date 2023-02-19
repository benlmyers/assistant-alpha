import json
from prompts.subdivision import subdivision_prompt
from prompts.io_step import io_step_prompt
from prompts.get_operations import get_operations_prompt
from prompts.get_parameters import get_parameters_prompt
from prompts.get_body import get_body_prompt
from prompts.get_next_step_context import get_next_step_context_prompt
from prompts.get_next_substep_context import get_next_substep_context_prompt
from prompts.get_service import get_service_prompt
from api_handling.get_service import get_available_services
from api_handling.get_body import get_body_spec_data
from api_handling.get_operations import get_endpoints_openapi
from api_handling.get_spec import get_spec
from api_handling.get_operations import get_endpoints_str


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

    f = open('train/training_elements.json')
    all_elements = json.loads(f.read())
    f.close()

    print('> Generating training data...')

    for process in execute_processes:
        training_pairs = []

        for elements in all_elements[process]:
            completion = elements['result']
            del elements['result']
            args = elements
            try:
                prompt = get_prompt(process, args)
            except KeyError as e:
                print('[!] Missing key for ' + process + ': ' + str(e))
                continue
            training_pairs.append({"prompt": prompt, "completion": completion})

        # Write to file /train/out/<process>.json
        f = open(f'train/out/{process}.json', 'w')
        f.write(json.dumps(training_pairs, indent=4))
        f.close()

        print('> Wrote ' + str(len(training_pairs)) +
              ' training pairs for ' + process + '.')

    print('> Generated training data.')


def get_prompt(process, args):
    if process == 'subdivision':
        return subdivision_prompt(**args, pretrain=True)
    elif process == 'io':
        return io_step_prompt(**args, pretrain=True)
    elif process == 'get_service':
        available_services = get_available_services()
        return get_service_prompt(**args, available_services=available_services, pretrain=True)
    elif process == 'get_operations':
        spec_data = get_spec(args['service'])
        endpoints = get_endpoints_openapi(spec_data)
        endpoints_str = get_endpoints_str(endpoints)
        return get_operations_prompt(**args, endpoints_str=endpoints_str, pretrain=True)
    elif process == 'get_parameters':
        return get_parameters_prompt(**args, pretrain=True)
    elif process == 'get_body':
        body_data = get_body_spec_data(args['service'], args['operation'])
        del args['operation']
        return get_body_prompt(**args, body_data=body_data, pretrain=True)
    elif process == 'get_next_step_context':
        return get_next_step_context_prompt(**args, pretrain=True)
    elif process == 'get_next_substep_context':
        return get_next_substep_context_prompt(**args, pretrain=True)
    else:
        return ''
