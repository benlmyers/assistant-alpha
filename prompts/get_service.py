def get_service_prompt(**kwargs):

    return example(**kwargs) + f"""Task: {kwargs['user_input']}
Service Step: {kwargs['step']}

The following is a list of services available to use:
{kwargs['available_services']}

Service to use for this step:
"""


def example(**kwargs):

    if 'pretrain' in kwargs and kwargs['pretrain'] == True:
        return f"""The following is a step for a Task you (the Assistant) could complete in a single API call.

Available Services:
[twitter, gmail, google calendar, uber]

Selection: twitter


Task: Send an email to John Doe
Service Step: Send the email to the user's recipient (API)

Available Services:
[google calendar, gmail, twitter]

Selection: gmail


Task: Check the prices of Ubers from here to LAX
Service Step: Check the prices of Ubers from the user's current location to their destination (API)

Available Services:
[twitter, uber, gmail, google sheets]

Selection: uber


"""

    return ''
