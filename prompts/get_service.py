def get_service_prompt(user_input, step, available_services):

    return f"""The following is a step for a Task you (the Assistant) could complete in a single API call.

Task: Tweet something for me
Step to Focus on: Post the user's message on Twitter (API)

The following is a list of services available to use:
[Twitter, Gmail, Google Calendar, Uber]

The service that should be used for this step is:
Twitter


Task: Check the prices of Ubers from here to LAX
Step to Focus on: Check the prices of Ubers from the user's current location to their destination (API)

The following is a list of services available to use:
[Twitter, Uber, Gmail, Google Sheets]

The service that should be used for this step is:
Uber


Task: {user_input}
Step to Focus on: {step}

The following is a list of services available to use:
{available_services}

The service that should be used for this step is:
"""