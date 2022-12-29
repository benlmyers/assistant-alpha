def get_server(spec_source, spec_data):
    if spec_source == 'openapi':
        return spec_data['servers'][0]["url"]
    else:
        print('Specification source not supported.')
        return ''
