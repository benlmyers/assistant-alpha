def get_operations_prompt(basic_endpoints_str, user_input, step, all_steps):

    return f"""The following is a list of API operations:
{basic_endpoints_str}

For the Task and Step, list all operations to use from the above list.
At the end of the operation, provide a short summary in parentheses about the purpose of the operation.
If multiple operations are needed (i.e. grab a user ID before performing an action related to a user), list them in order.

Task: DM Lionel Messi a message on Twitter
All Steps: [Get the message to send (AI), Send the specified message to Lionel Messi (API)]
Step: Send the specified message to Lionel Messi (API)

GET /2/users/by/username/{{username}} (Obtain Lionel Messi's user ID)
POST /2/dm_conversations/with/{{participant_id}}/messages (Send a message to that ID)

Task: {user_input}
All Steps: {all_steps}
Step: {step}

"""
