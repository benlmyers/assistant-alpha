import openai
import json

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

retrain_processes = []

process_complexity = {
    'subdivision': 'davinci',
    'io': 'babbage',
    'get_service': 'curie',
    'get_operations': 'curie',
    'get_parameters': 'davinci',
    'get_body': 'davinci',
    'get_next_step_context': 'davinci',
    'get_next_substep_context': 'davinci'
}


def fine_tune():

    f = open('train/pretrained_models.json')
    data = json.loads(f.read())
    f.close()

    print('[TRAIN] Fine-tuning.')

    for process in execute_processes:

        if process not in data['models']:
            data['models'][process] = {}

        training = open(f'train/out/{process}.jsonl').readlines()

        if len(training) == 0:
            print('[!] No training data for ' + process + '. Skipping.')
            continue
        if process in retrain_processes:
            tune_from_base(process, data, training)
        elif 'model_id' in data['models'][process]:
            tune_from_pt(process, data, training)
        else:
            tune_from_base(process, data, training)

    with open('train/pretrained_models.json', 'w') as out:
        out.write(json.dumps(data, indent=4))
        out.close()


def upload_file(process, data, temp=False):

    process_name = process
    if temp:
        process_name = process + '_temp'

    print('> Uploading ' + process_name + '.jsonl to OpenAI...')

    try:
        upload_response = openai.File.create(
            file=open(f'train/out/{process_name}.jsonl', "rb"),
            purpose='fine-tune'
        )
    except openai.InvalidRequestError as e:
        print('[!] Error uploading ' +
              process_name + '.jsonl: ' + str(e))

    _id = upload_response['id']
    date = upload_response['created_at']

    print('> File ' + process_name + '.jsonl uploaded with id ' + _id + '.')

    data['models'][process]['file_id'] = _id
    data['models'][process]['date'] = date
    data['models'][process]['base'] = process_complexity[process]


def tune_from_pt(process, data, training):

    existing_pairs = data['models'][process]['pairs']

    if len(training) == existing_pairs:
        print('[!] No new training data for ' + process + '. Skipping.')
        return
    if 'model_id' not in data['models'][process]:
        print('[!] No model id for ' + process + '. Skipping.')
        return

    new_training = training[existing_pairs:]

    out = open(f'train/out/{process}_temp.jsonl', 'w')
    out.write(''.join(new_training))
    out.close()

    upload_file(process, data, temp=True)

    pt = data['models'][process]['model_id']
    base = data['models'][process]['base']
    file_id = data['models'][process]['file_id']

    print('> Refining ' + process + ' with pre-tuned model ' +
          pt + ' (base source: ' + base + ')...')

    try:
        result = openai.FineTune.create(training_file=file_id,
                                        model=pt, suffix=process)
    except openai.InvalidRequestError as e:
        print('[!] Error refining ' + process + ': ' + str(e))
        return

    print('> Fine-tuning ' + process + ' completed.')

    data['models'][process]['model_id'] = result['id']
    data['models'][process]['pairs'] = data['models'][process]['pairs'] + \
        len(training)


def tune_from_base(process, data, training):

    upload_file(process, data)

    file_id = data['models'][process]['file_id']
    base = data['models'][process]['base']

    print('> Fine-tuning ' + process + ' with base model ' + base + '...')

    result = openai.FineTune.create(training_file=file_id,
                                    model=base, suffix=process)

    print('> Fine-tuning ' + process + ' completed.')

    data['models'][process]['model_id'] = result['id']
    data['models'][process]['pairs'] = len(training)
