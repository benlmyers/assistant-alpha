import json

from api_handling.get_security import get_security


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

    # if specification_source == 'openapi':
    data = remove_component_references_openapi(data, data)

    spec_f.close()

    return specification_source, data


def remove_component_references_openapi(orig_data, data):

    # Remove all nested objects with key "$ref"
    if isinstance(data, dict):
        for key in list(data.keys()):
            if is_reference_object(data[key]):
                data[key] = get_component_openapi(orig_data, data[key]['$ref'])
            else:
                remove_component_references_openapi(orig_data, data[key])
    elif isinstance(data, list):
        for index in range(len(data)):
            if is_reference_object(data[index]):
                data[index] = get_component_openapi(
                    orig_data, data[index]['$ref'])
            else:
                remove_component_references_openapi(orig_data, data[index])

    return data


def is_reference_object(data):
    if isinstance(data, dict) and '$ref' in data.keys():
        return True
    return False


def get_component_openapi(data, path):

    path = path.split('/')

    if path[0] != '#':
        return {}

    path.pop(0)

    data_slice = data

    for key in path:
        data_slice = data_slice[key]

    return data_slice
