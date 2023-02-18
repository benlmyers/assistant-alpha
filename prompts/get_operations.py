def get_operations_prompt(**kwargs):

    return example(**kwargs) + f"""Task: {kwargs['user_input']}
All Steps: {kwargs['all_steps']}
Step: {kwargs['step']}
Operations:

"""


def example(**kwargs):

    if kwargs['pretrain'] and kwargs['pretrain'] == True:
        return f"""The following is a list of API operations:
{kwargs['endpoints_str']}

For the Task and Step, list all operations to use from the above list.
At the end of the operation, provide a short summary in parentheses about the purpose of the operation.
If multiple operations are needed (i.e. grab a user ID before performing an action related to a user), list them in order.

Task: DM Lionel Messi a message on Twitter
All Steps: [Get the message to send (AI), Send the specified message to Lionel Messi (API)]
Step: Send the specified message to Lionel Messi (API)
Operations:

GET /2/users/by/username/{{username}} (Obtain Lionel Messi's user ID)
POST /2/dm_conversations/with/{{participant_id}}/messages (Send a message to that ID)

Task: Get my user info on Twitter
All Steps: [Get my user info (API), Summarize my user info (AI)]
Step: Get my user info (API)
Operations:

GET /2/users/me (Obtain user data)

"""

    return ''
