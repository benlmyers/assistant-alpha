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

        if mode in training_elements_data:
            arr = training_elements_data[mode]

            for dict in arr:
                dict_copy = True
                for key in dict:
                    if dict[key] and key != 'result' and dict[key] != kwargs[key]:
                        dict_copy = False
                if dict_copy:
                    return correct_result

            new_data = kwargs
            new_data['result'] = correct_result
            arr.append(new_data)
            new_training_elements_data = json.dumps(
                training_elements_data, indent=4)
            with open('train/training_elements.json', 'w') as out:
                out.write(new_training_elements_data)

        return correct_result
