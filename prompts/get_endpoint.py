def get_endpoint_prompt(basic_endpoints_str, user_input, step):

    return f"""The following is a list of API endpoint paths, their methods and a quick summary about each of them:
{basic_endpoints_str}

The following is a Step for a Task you (the Assistant) could complete in a single API call.

Task: DM Lionel Messi a message
Step: Send the message to the specified user (API)

Chosen from the above endpoints list, here's the path and method to use, summary omitted:
POST /2/dm_conversations/with/{{participant_id}}/messages

Task: {user_input}
Step: {step}

Chosen from the above endpoints list, here's the path and method to use, summary omitted:
"""
