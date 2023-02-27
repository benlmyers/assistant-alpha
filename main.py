import openai

import sec
from step.ai_step import ai_step
from step.api_step import api_step
from step.io_step import io_step
from subdivision import subdivision

openai.api_key = sec.OPENAI_API_KEY
openai.organization = sec.OPENAI_ORGANIZATION_ID

# 1. Should the Assistant collect training reinforcements from the user?
TRAINING_MODE = True
# 2. Should training run? That is, should the Training Elements be converted to training data?
RUN_TRAINING = True
# 3. Should fine tuning run? That is, should OpenAI's models be fine-tuned to our training data?
RUN_FINE_TUNING = True

###

if RUN_TRAINING:
    from train.generate_training_data import generate_training_data
    generate_training_data()
    print('')

if RUN_FINE_TUNING:
    from train.fine_tune import fine_tune
    fine_tune()
    print('')

# An array to keep a running total of the cost of the Assistant's actions.
cost = []

user_input = input('Enter a command: ')

print('[...]')
steps = subdivision(user_input, cost)

count = 0
total_steps = len(steps)

# Context data keeps track of the data that the Assistant has collected so far.
context_data = '[No data]'

# Execute the steps.
for step in steps:
    count += 1
    print(f'Step {count} of {total_steps}: {step}')
    if '(API)' in step:
        print('[...]')
        context_data = api_step(user_input, step, steps, context_data, cost)
    elif '(IO)' in step:
        print('[...]')
        context_data = io_step(step, cost)
    elif '(AI)' in step:
        print('[...]')
        context_data = ai_step(user_input, step, context_data, cost)
        print('Result:')
        print(context_data)

print('> Done.')

# Aggregate the total cost.
total_tokens = 0
total_cost = 0.0
for item in cost:
    total_tokens += item[0]
    total_cost += item[1]

print('> Total token cost: ' + str(total_tokens) +
      ' ($' + str(round(total_cost, 2)) + ')')
