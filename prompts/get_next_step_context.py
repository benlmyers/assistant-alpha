def get_next_step_context_prompt(**kwargs):

    return f"""The following is the current user input:
User Input: "Post a summary this week's Google Calendar events on Twitter"

This is the current step in processing the user input:
Step: "Post the summary on Twitter"

The response from the current step that needs to be sent as context to the next step is:
Response: {{"data": {{"id": "123456789"}}}}

Processing the response, the context to be sent to the next step is:
Post tweeted with ID: 123456789

The following is the current user input:
User Input: {kwargs['user_input']}

This is the current step in processing the user input:
Step: {kwargs['step']}

The response from the current step that needs to be sent as context to the next step is:
Response: {kwargs['response']}

Processing the response, the context to be sent to the next step is:

"""
