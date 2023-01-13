from openai.api_resources.completion import Completion
from models import DAVINCI
from models import log_cost


def subdivision(user_input, cost):

    model = DAVINCI
    max_tokens = 512

    prompt = f"""The following are user requests simplified into a list of tasks you (the Assistant) could complete using API's or text completions.

If any API calls are needed for each Task, add "(API)" at the end of the task. Use "(API)" only when needed. Each task should pertain to a single Service, like Google or Twitter, and not multiple.

Else, if additional data or input is needed, add "(IO)" at the end of the task. Examples for IO include user input, location, calendar events, etc. IO should only be used when absolutely necessary.

Otherwise, if you can handle the task with no API call needed, using the context of the previous steps, add "(AI)" at the end of the task.

User Request: Add events from today's inbox into my calendar.

Response:
Get the user's emails from today's inbox (API),
Extract the events from the user emails (AI),
For each event, add it in the user's calendar (API)

User Request: Create a budget for me using Google Sheets.

Response:
Create a new Google Drive spreadsheet (API),
Add headers for the budget categories (API),
Add rows for sample budget items (API)

User Request: Check the prices of Ubers from here to LAX.

Response:
Get the user's current location (IO),
Get the user's destination (API),
Check the prices of Ubers from the user's current location to their destination (API)

User Request: Summarize a paragraph for me.

Response:
Get a paragraph from the user (IO),
Summarize the paragraph (AI)

User Request: Send a DM to my friend on Twitter.

Response:
Get the user's friend's Twitter handle (IO),
Send a DM to the user's friend on Twitter (API)

User Request: {user_input}

Response:
"""

    # Get completion
    completion = Completion.create(
        model=model,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=0,
        stop='\n\n'
    )

    # Grab the steps from the completion.
    # The steps are comma-seperated, and in between the characters '[' and ']'.
    result = completion.choices[0]
    result = result.text

    log_cost(completion, cost)

    if ',' in result:
        steps = result.split(',')
    else:
        steps = [result]

    formatted_steps = [step.strip() for step in steps]

    return formatted_steps
