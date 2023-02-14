def io_step_prompt(step):
    return f"""
Classify the input/output items into one of the following categories:

Text Input, Geolocation, Time

Get today's date
Category: Time

Get the user's current location
Category: Geolocation

Get a paragraph input
Category: Text Input

Search Tweets
Category: Text Input

Get the user's friend's Instagarm handle
Category: Text Input

{step}
Category:"""
