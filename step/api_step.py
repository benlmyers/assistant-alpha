from api_handling.get_operations import get_operations
from api_handling.get_parameters import get_parameters
from api_handling.get_body import get_body
from api_handling.get_service import get_service
from api_handling.get_spec import get_spec
from api_handling.get_security import get_security
from api_handling.get_server import get_server
from api_handling.send_request import send_request
from api_handling.get_next_step_context import get_next_step_context
from api_handling.get_next_substep_context import get_next_substep_context


def api_step(user_input, step, all_steps, context_data, cost):

    # This context data can be modified with new information from the API response.
    _context_data = context_data

    # Get the relevant service i.e. Twitter, Google Calendar, etc.
    service = get_service(user_input, step, cost)

    print('> Getting operations for ' + service + '...')

    # Get the specification source and data for the specific service.
    # For example, for Twitter, spec_source = "openapi" and spec_data is the JSON data from specifications/openapi/twitter.json
    spec_source, spec_data = get_spec(service)

    # Get the operations needed for the API request.
    # For example, "GET /2/compliance/jobs (goal)"
    raw_operations = get_operations(
        user_input, step, all_steps, spec_source, spec_data, service, cost)

    server = get_server(spec_source, spec_data)

    print('> Using server ' + server)

    raw_operations = raw_operations.split('\n')

    for i, raw_operation in enumerate(raw_operations):
        # Extract the endpoint and method from the above operation string.
        # For example, "/2/compliance/jobs"
        endpoint = raw_operation.split(' ')[1].strip()
        # For example, "get"
        method = raw_operation.split(' ')[0].strip().lower()
        # Get text inside ( )
        substep = raw_operation.split('(')[1].split(')')[0].strip()

        print('> Performing substep ' + str(i+1) + ' of ' +
              str(len(raw_operations)) + ': ' + substep)

        # Step description (substep description)
        detailed_step = step + ' - ' + substep

        operation_data = spec_data['paths'][endpoint][method.lower()]

        print('> Getting parameters...')
        # Get the parameters data for the request.
        path_params, query_params = get_parameters(
            user_input, detailed_step, _context_data, operation_data, cost)

        body_data = {}
        if (method == 'post'):
            print('> Getting request body...')

            # Get the parameters data for the request.
            body_data = get_body(
                user_input, detailed_step, _context_data, operation_data, cost)

        print('> Getting authorization...')

        auth, auth_loc = get_security(operation_data, spec_data, service)

        print('> Sending request...')

        response = send_request(server, endpoint, method,
                                path_params, query_params, body_data, auth, auth_loc)

        print('> Response: ' + str(response.status_code))
        print(response.text)

        if str(response.status_code).startswith('4'):
            print('> An issue occured. Operation failed.')
            return

        response = response.text

        if i < len(raw_operations) - 1:
            print('> Getting context data for next operation...')

            next_substep = raw_operations[i +
                                          1].split('(')[1].split(')')[0].strip()

            # There is another substep, grab the relevant context data for use in the next substep.
            # Example:
            # user_input = "Send a DM to Lionel Messi"
            # step = "Send the message to Lionel Messi on Twitter"
            # substep 1 = "Get Lionel Messi's Twitter user ID"
            # substep 2 = "Send the message to the specified user ID"
            # response (for substep 1) = {"data": {"id": "123456789"}} or something similar
            # AI should parse response and return substep_data = "ID: 123456789"
            substep_data = get_next_substep_context(
                user_input, step, substep, next_substep, response, cost)

            # Set _context_data to the current context data + the new context data from the substep.
            # So _context_data can be used correctly in the next substep.
            _context_data = _context_data + '\n' + substep_data

    # After all substeps in a step are completed, return the relevant context data.
    # Example 1:
    # user_input = "Post a summary this week's Google Calendar events on Twitter"
    # step = "Get this week's calendar events from Google Calendar"
    # response = {"data": {"items": [{"summary": "Meeting with John"}, {"summary": "Meeting with Jane"}]}}
    # Return Value: "Meeting with John and Jane"
    # Example 2:
    # user_input = "Post a summary this week's Google Calendar events on Twitter"
    # step = "Post the summary on Twitter"
    # response = {"data": {"id": "123456789"}} (the twitter Post ID)
    # Return Value: "Post tweeted with ID: 123456789"
    return get_next_step_context(user_input, step, response, cost)
