def get_service_prompt(user_input, step, available_services):

    return f"""Task: Tweet something for me
Service Step: Post the user's message on Twitter (API)

Available Services:
[twitter, gmail, google calendar, uber]

Selection:
twitter


Task: Send an email to John Doe
Service Step: Send the email to the user's recipient (API)

Available Services:
[google calendar, gmail, twitter]

Selection:
gmail


Task: Check the prices of Ubers from here to LAX
Service Step: Check the prices of Ubers from the user's current location to their destination (API)

Available Services:
[twitter, uber, gmail, google sheets]

Selection:
uber


Task: {user_input}
Service Step: {step}

Selection:
{available_services}

Service to use for this step:
"""
