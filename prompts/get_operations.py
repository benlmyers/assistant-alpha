def get_operations_prompt(basic_endpoints_str, user_input, step):

    return f"""The following is a list of API endpoint paths, their methods and a quick summary about each of them:
{basic_endpoints_str}

For the Task and Step, list the endpoint path and method to use, and the intention in use with the Step. Choose endpoints OTHER THAN STREAMS. Each chosen endpoint must server a purpose, so any subsequent endpoints should rely on the previous ones.

Task: DM Lionel Messi a message on Twitter
Step: Send the specified message to Lionel Messi (API)

GET /2/users/by/username/{{username}} (Obtain Lionel Messi's user ID)
POST /2/dm_conversations/with/{{participant_id}}/messages (Send a message to that ID)

Task: {user_input}
Step: {step}

"""
