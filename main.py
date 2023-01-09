import openai

import sec
from step.ai_step import ai_step
from step.api_step import api_step
from step.io_step import io_step
from subdivision import subdivision

openai.api_key = sec.OPENAI_API_KEY
openai.organization = sec.OPENAI_ORGANIZATION_ID

user_input = input('Enter a command: ')

print('[...]')
steps = subdivision(user_input)

count = 0
total_steps = len(steps)

context_data = '[No data]'


for step in steps:
    count += 1
    print(f'Step {count} of {total_steps}: {step}')
    if '(API)' in step:
        print('[...]')
        context_data = api_step(user_input, step, context_data)
    elif '(IO)' in step:
        print('[...]')
        context_data = io_step(step)
    elif '(AI)' in step:
        print('[...]')
        context_data = ai_step(user_input, step, context_data)
        print('Result:')
        print(context_data)
