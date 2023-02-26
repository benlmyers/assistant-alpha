import openai
import json


def fine_tune():

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

    f = open('train/pretrained_models.json')
    data = json.loads(f.read())
    f.close()

    print('[TRAIN] Fine-tuning.')

    for process in execute_processes:

        training = open(f'train/out/{process}.jsonl').readlines()

        if len(training) == 0:
            print('[!] No training data for ' + process + '. Skipping.')
            continue
        if process in retrain_processes:
            tune_from_base(process, data, training)
        elif 'model_id' in data['models'][process]:
            tune_from_pt(process, data, training)
        else:
            tune_from_base(process, data)

    with open('train/pretrained_models.json', 'w') as out:
        out.write(json.dumps(data, indent=4))
        out.close()


def upload_file(process, data):

    print('> Uploading ' + process + '.jsonl to OpenAI...')

    try:
        upload_response = openai.File.create(
            file=open(f'train/out/{process}.jsonl', "rb"),
            purpose='fine-tune'
        )
    except openai.InvalidRequestError as e:
        print('[!] Error uploading ' +
              process + '.jsonl: ' + str(e))

    _id = upload_response['id']
    date = upload_response['created_at']

    print('> File ' + process + '.jsonl uploaded with id ' + _id + '.')

    if process not in data['models']:
        data['models'][process] = {}

    data['models'][process]['file_id'] = _id
    data['models'][process]['date'] = date


def tune_from_pt(process, data, training):

    existing_pairs = data['models'][process]['pairs']

    if len(training) == existing_pairs:
        print('[!] No new training data for ' + process + '. Skipping.')
        return
    if 'model_id' not in data['models'][process]:
        print('[!] No model id for ' + process + '. Skipping.')
        return

    new_training = training[existing_pairs:]

    print('> Uploading ' + process + '_temp.jsonl to OpenAI...')

    out = open(f'train/out/{process}_temp.jsonl', 'wrb')
    out.write(''.join(new_training))
    out.close()

    try:
        upload_response = openai.File.create(
            file=open(f'train/out/{process}_temp.jsonl', "rb"),
            purpose='fine-tune',
            model=data['models'][process]['model_id']
        )
    except openai.InvalidRequestError as e:
        print('[!] Error uploading ' +
              process + '.jsonl: ' + str(e))
        return

    print('> File ' + process + '.jsonl uploaded with id ' + _id + '.')


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
