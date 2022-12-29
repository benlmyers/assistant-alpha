def get_operations_prompt(basic_endpoints_str, user_input, step):

    return f"""The following is a list of API endpoint paths, their methods and a quick summary about each of them:
{basic_endpoints_str}

The following is a Step for a Task you (the Assistant) could complete in a single API call.

Task: DM Lionel Messi a message on Twitter
Step: Send the specified message to Lionel Messi (API)

Chosen from the above endpoints list, here's the paths and methods to use, and the intention in use with the Step:
GET /2/users/by/username/{{username}} (Obtain Lionel Messi's user ID)
POST /2/dm_conversations/with/{{participant_id}}/messages (Send a message to the user ID)

Task: {user_input}
Step: {step}

Chosen from the above endpoints list, here's the paths and methods to use, and the intention in use with the Step:
"""
