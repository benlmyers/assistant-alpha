def get_next_substep_context_prompt(user_input, step, substep, next_substep, response):

    return f"""The following is the current user input:
User Input: "Send a DM to Lionel Messi"

This is the current step in processing the user input:
Step: "Send the message to Lionel Messi on Twitter"

These are the current and upcoming substeps for processing the current step:
Current Substep: "Get Lionel Messi's Twitter user ID"
Next Substep: "Send the message to the specified user ID"

The response from the current substep that needs to be sent as context to the next substep is:
Response: {{"data": {{"id": "123456789"}}}}

Processing the response, the context to be sent to the next substep is:
ID: 123456789

The following is the current user input:
User Input: {user_input}

This is the current step in processing the user input:
Step: {step}

These are the current and upcoming substeps for processing the current step:
Current Substep: {substep}
Next Substep: {next_substep}

The response from the current substep that needs to be sent as context to the next substep is:
Response: {response}

Processing the response, the context to be sent to the next substep is:

"""