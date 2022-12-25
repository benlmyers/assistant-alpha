# A class representing a basic endpoint.
# Each endpoint has a path, methods and a summary of what they do.
class Endpoint:

    # The path of the endpoint
    # e.g. "/2/users/{{id}}/followed_lists"
    path = '/'

    # The operations and summaries of what they do
    # e.g. "(GET) Get User's Followed Lists"
    operations = []
