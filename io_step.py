import datetime
import subprocess

from openai import Completion

from models import BABBAGE


def io_step(step):

    model = BABBAGE
    max_tokens = 128

    prompt = f"""
Classify the input/output items into one of the following categories:

Text Input, Geolocation, Time

Get today's date
Category: Time

Get the user's current location
Category: Geolocation

Get a paragraph input
Category: Text Input

Get what time it is now
Category: Time

{step}
Category:"""

    # Get completion
    completion = Completion.create(
        model=model,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=0
    )

    # Grab only the new text from the completion, after the last colon.
    result = completion.choices[0]
    category = result.text.split(':')[-1].strip()

    print('[Category] ' + category)

    if category == "Time":
        # Get today's date
        # Category: Time
        return datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    elif category == "Geolocation":
        # Get the user's current location
        # Call curl GET ipinfo.io/loc
        loc = subprocess.run(["curl", "GET", "ipinfo.io/loc"],
                             capture_output=True).stdout.decode('utf-8')
        return loc
    elif category == "Text Input":
        # Get a paragraph input
        # Category: Text Input
        return input("Enter text: ")
    else:
        raise Exception("Invalid category")
