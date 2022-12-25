import json


def get_spec(service):

    # Load the service data.
    service_f = open('services.json')
    data = json.loads(service_f.read())

    service = service.lower()
    specification_source = '[Not Found]'

    # Get the specification source of the specified service.
    # For instance, Twitter uses OpenAPI Specification.
    # In this example, specification_source = "openapi".
    for service_data in data:
        if service_data['name'] == service:
            specification_source = service_data['specProvider']

    print('> Reading specification from ' + specification_source)

    # Get the file path of the specification json
    # The specifications are located at specifications/SOURCE/SERVICE.json.
    # For example, Twitter is located at specifications/openapi/twitter.json.
    spec_file_name = 'specifications/' + \
        specification_source + '/' + service + '.json'

    # Load the data from the specification
    spec_f = open(spec_file_name)
    data = json.loads(spec_f.read())

    spec_f.close()

    return specification_source, data
