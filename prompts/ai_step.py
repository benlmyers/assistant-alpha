def ai_step_prompt(user_input, step, context_data):
    return f"""The following is a step for a Task you (the Assistant) could complete in a single AI text completion: this one.

Task: {user_input}
Step to Focus on: {step}
Relevant Context Data:
{context_data}

Correct completion data result:

"""
