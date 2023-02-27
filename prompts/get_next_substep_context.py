def get_next_substep_context_prompt(**kwargs):

    return example(**kwargs) + f"""The following is the current user input:
User Input: {kwargs['user_input']}

This is the current step in processing the user input:
Step: {kwargs['step']}

These are the current and upcoming substeps for processing the current step:
Current Substep: {kwargs['substep']}
Next Substep: {kwargs['next_substep']}

The response from the current substep that needs to be sent as context to the next substep is:
Response: {kwargs['response']}

Processing the response, the context to be sent to the next substep is:

"""


def example(**kwargs):

    if 'pretrain' not in kwargs or not kwargs['pretrain']:
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

"""

    return ''
