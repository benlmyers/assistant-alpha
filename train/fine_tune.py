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

    print('[TRAIN] Beginning fine tuning.')

    f = open('train/pretrained_models.json')
    pretrained_models_data = json.loads(f.read())
    f.close()

    for process in execute_processes:

        data = open(f'train/out/{process}.jsonl').readlines()

        if len(data) == 0:
            print('[!] No data for ' + process + '. Skipping.')
            continue

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

        if process not in pretrained_models_data['models']:
            pretrained_models_data['models'][process] = {}

        pretrained_models_data['models'][process]['file_id'] = _id
        pretrained_models_data['models'][process]['date'] = date
        pretrained_models_data['models'][process]['pairs'] = len(data)

    with open('train/pretrained_models.json', 'w') as out:
        out.write(json.dumps(pretrained_models_data, indent=4))
        out.close()
