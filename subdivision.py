from openai.api_resources.completion import Completion


def subdivision(user_input):

    model = "text-davinci-003"
    max_tokens = 512

    prompt = f"""
  The following are user requests simplified into a list of tasks you (the Assistant) could
  complete in a single API call, or AI text completion.

  If any API call is needed for each Task, add "(API)" at the end of the task.
  Use "(API)" only when needed.

  Else, if additional data or input is needed, add "(IO)" at the end of the task.
  Examples for IO include user input, location, calendar events, etc.
  IO should only be used when absolutely necessary.

  Otherwise, if an AI robot like GPT-3 can handle the task with no API call needed, 
  using the context of the previous steps, add "(AI)" at the end of the task.

  User Request: Add events from today's inbox into my calendar.

  Response: [
    Get the user's emails from today's inbox (API),
    Extract the events from the user emails (AI),
    For each event, add it in the user's calendar (API)
  ]

  User Request: Create a budget for me using Google Sheets.

  Response: [
    Create a new Google Drive spreadsheet (API),
    Add headers for the budget categories (API),
    Add rows for sample budget items (API)
  ]

  User Request: Check the prices of Ubers from here to LAX.

  Response: [
    Get the user's current location (IO),
    Get the user's destination (API),
    Check the prices of Ubers from the user's current location to their destination (API)
  ]

  User Request: Summarize a paragraph for me.

  Response: [
    Get a paragraph from the user (IO),
    Summarize the paragraph (AI)
  ]

  User Request: {user_input}

  Response: 
  """

    # Get completion
    completion = Completion.create(
        model=model,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=0
    )

    # Grab the steps from the completion.
    # The steps are comma-seperated, and in between the characters '[' and ']'.
    result = completion.choices[0]

    try:
        steps = result.text.split('[')[1].split(']')[0]
        if ',' in steps:
            steps = steps.split(',')
        steps = [step.strip() for step in steps]
    except Exception:
        steps = []
        raise Exception("Invalid steps. Completion: \"" + result.text + "\"")

    return steps
