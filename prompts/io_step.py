def io_step_prompt(**kwargs):
    return f"""Classify the input/output items into one of the following categories:

Text Input, Geolocation, Time

{example(**kwargs)}{kwargs['step']}
Category:"""


def example(**kwargs):

    if kwargs['pretrain'] and kwargs['pretrain'] == True:
        return f"""Get today's date
Category: Time

Get the user's current location
Category: Geolocation

Get a paragraph input
Category: Text Input

Search Tweets
Category: Text Input

Get the user's friend's Instagarm handle
Category: Text Input

"""
