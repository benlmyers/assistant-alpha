import datetime
import subprocess

from openai import Completion

from models import BABBAGE
from models import log_cost

from train.train_from import train_from
from prompts.io_step import io_step_prompt


def io_step(step, cost):

    model = BABBAGE
    max_tokens = 8

    prompt = io_step_prompt(step=step)

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

    log_cost(completion, cost)

    category = train_from(category, "io", step=step)

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
        print('[!] Warning: Invalid category.')
        return input("Enter text: ")
