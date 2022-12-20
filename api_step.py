import json
from BasicEndpoint import BasicEndpoint
import itertools as IT

from openai.api_resources.completion import Completion

from models import ADA
from models import BABBAGE


def api_step(user_input, step, context_data):

    service = get_service(user_input, step)
    
    print('Picking an endpoint for ' + service + '...')
    
    endpoint = get_endpoint(user_input, step, service)


def get_service(user_input, step):
    model = ADA
    max_tokens = 128

    available_services = get_available_services()

    prompt = f"""
The following is a step for a Task you (the Assistant) could complete in a single API call.

Task: Tweet something for me
Step to Focus on: Post the user's message on Twitter (API)

The following is a list of services available to use:
[Twitter, Gmail, Google Calendar, Uber]

The service that should be used for this step is:
Twitter


Task: Check the prices of Ubers from here to LAX
Step to Focus on: Check the prices of Ubers from the user's current location to their destination (API)

The following is a list of services available to use:
[Twitter, Uber, Gmail, Google Sheets]

The service that should be used for this step is:
Uber


Task: {user_input}
Step to Focus on: {step}

The following is a list of services available to use:
{available_services}

The service that should be used for this step is:
"""

    # Get completion
    completion = Completion.create(
        model=model,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=0
    )

    return completion.choices[0].text


def get_endpoint(user_input, step, service):

    model = BABBAGE
    max_tokens = 128

    service_f = open('services.json')
    data = json.loads(service_f.read())

    service = service.lower()
    specification_source = '[Not Found]'

    for service_data in data:
        if service_data['name'] == service:
            specification_source = service_data['specProvider']

    print('> Reading specification from ' + specification_source)

    spec_f = open('specifications/' + specification_source +
                  '/' + service + '.json')
    data = json.loads(spec_f.read())

    basic_endpoints = get_basic_endpoints_openapi(data)
    spec_f.close()

    print('> Choosing the best endpoint to use')

    basic_endpoints_str_arr = []

    for endpoint in basic_endpoints:
        basic_endpoints_str = ''
        basic_endpoints_str = basic_endpoints_str + f"""

Path: {endpoint.path} ({endpoint.method})
Summary: {endpoint.summary}

"""
        basic_endpoints_str_arr.append(basic_endpoints_str)

    prompt = f"""
The following is a step for a Task you (the Assistant) could complete in a single API call.

Task: Block barstoolspots on Twitter for me
Step to Focus on: Get the specified user's ID (API)

The following is a list of API endpoint paths, their methods and a quick summary about each of them:
[
    
    Path: /2/tweets/{{id}}/liking_users (get)
    Summary: Returns User objects that have liked the provided Tweet ID
    
    ,
    
    Path: /2/tweets/{{id}}/quote_tweets (get)
    Summary: Retrieve Tweets that quote a Tweet.
    
    ,
    
    Path: /2/tweets/{{id}}/retweeted_by (get)
    Summary: Returns User objects that have retweeted the provided Tweet ID
    
    ,
    
    Path: /2/tweets/{{tweet_id}}/hidden (put)
    Summary: Hide replies
    
    ,
    
    Path: /2/users (get)
    Summary: User lookup by IDs,

    ,
    
    Path: /2/users/by (get)
    Summary: User lookup by usernames
    
    ,
    
    Path: /2/users/by/username/{{username}} (get)
    Summary: User lookup by username

]

And the following is the chosen path and method from above to use for the step:
Path: /2/users/by/username/{{username}} (get)
Summary: User lookup by username




Task: Follow Lionel Messi on Twitter for me
Step to Focus on: Follow the specified user (API)

The following is a list of API endpoint paths, their methods and a quick summary about each of them:
[
    
    Path: /2/users/{{id}}/followed_lists (get)
    Summary: Get User's Followed Lists
    
    ,
    
    Path: /2/users/{{id}}/followed_lists (post)\
    Summary: Follow a List
    
    ,


    Path: /2/users/{{id}}/followed_lists/{{list_id}} (delete)
    Summary: Unfollow a List
    
    ,
    
    Path: /2/users/{{id}}/followers (get)
    Summary: Followers by User ID
    
    ,

    Path: /2/users/{{id}}/following (get)
    Summary: Following by User ID
    
    ,
    
    Path: /2/users/{{id}}/following (post)
    Summary: Follow User
    
    ,

    Path: /2/users/{{id}}/liked_tweets (get)
    Summary: Returns Tweet objects liked by the provided User ID

]

And the following is the chosen path and method from above to use for the step:
Path: /2/users/{{id}}/following (post)
Summary: Follow User




Task: {user_input}
Step to Focus on: {step}

The following is a list of API endpoint paths, their methods and a quick summary about each of them:
{basic_endpoints_str}

And the following is the chosen path and method from above to use for the step:\n
"""

    completion = Completion.create(
        model=model,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=0
    )

    endpoint_result = completion.choices[0].text

    print('> Found endpoint: ' + endpoint_result)
    return endpoint_result


def get_available_services():

    f = open('services.json')
    data = json.loads(f.read())

    available_services = []

    for item in data:
        available_services.append(item["name"])

    f.close()

    return available_services


def get_basic_endpoints_openapi(data):

    basic_endpoints = []

    for path, path_data in data['paths'].items():
        for method, method_data in path_data.items():
            endpoint = BasicEndpoint()
            endpoint.path = path
            endpoint.method = method
            endpoint.summary = path_data[method]['summary']
            basic_endpoints.append(endpoint)

    return basic_endpoints
