def ai_step_prompt(**kwargs):
    return f"""The following is a step for a Task you (the Assistant) could complete in a single AI text completion: this one.

Task: {kwargs['user_input']}
Step to Focus on: {kwargs['step']}
Relevant Context Data:
{kwargs['context_data']}

Correct completion data result:

"""
