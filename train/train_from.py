import json

from settings import TRAINING_MODE


def train_from(result, mode, **kwargs):

    if TRAINING_MODE:
        print('[TRAIN] Completion:')
        print(result)
        training_correct = input('[TRAIN] Is this correct? (Y/n/i): ')

        if training_correct.lower() == 'n':
            print('[TRAIN] Please correct the completion:')
            correct_result = input()
        elif training_correct.lower() == 'i':
            print('[TRAIN] Skipping data recording.')
            return result
        else:
            correct_result = result

        f = open('train/training_elements.json')
        training_elements_data = json.loads(f.read())
        f.close()

        if (training_elements_data[mode] != None):
            arr = training_elements_data[mode]

            exists = False
            for data in arr:
                if data['user_input'] == kwargs['user_input']:
                    exists = True
                    break
            if exists:
                return correct_result

            new_data = kwargs
            new_data['result'] = correct_result
            arr.append(new_data)
            new_training_elements_data = json.dumps(
                training_elements_data, indent=4)
            with open('train/training_elements.json', 'w') as out:
                out.write(new_training_elements_data)

        return correct_result
