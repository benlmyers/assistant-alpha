import openai

import sec
from step.ai_step import ai_step
from step.api_step import api_step
from step.io_step import io_step
from subdivision import subdivision

openai.api_key = sec.OPENAI_API_KEY
openai.organization = sec.OPENAI_ORGANIZATION_ID

cost = []

user_input = input('Enter a command: ')

print('[...]')
steps = subdivision(user_input, cost)

count = 0
total_steps = len(steps)

context_data = '[No data]'


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

total_tokens = 0
total_cost = 0.0

for item in cost:
    total_tokens += item[0]
    total_cost += item[1]

print('> Total token cost: ' + str(total_tokens) +
      ' ($' + str(round(total_cost, 2)) + ')')
