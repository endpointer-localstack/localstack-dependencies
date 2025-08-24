import json
from urllib.parse import parse_qs

RESPONSE_STATUS = 'response_status'
RESPONSE_HEADERS = 'response_headers'
RESPONSE_BODY = 'response_body'
CONTENT_LENGTH = 'Content-Length'
CONTENT_TYPE = 'Content-Type'
UTF_8 = 'utf-8'
APPLICATION_JSON = 'application/json'
CLIENT_IP = 'client_ip'

def get_request_verb(environ):
    
    request_verb = environ.get('REQUEST_METHOD')
    return request_verb

def get_request_headers(environ):
    
    request_headers = {}

    for k,v in environ.items():

        key = str(k).lower().replace('_', '-')

        is_http = key.startswith('http-')
        if is_http:
            new_key = key[5:]
            request_headers[new_key] = v

    request_headers[CLIENT_IP] = environ['REMOTE_ADDR']

    return request_headers

def get_client_ip(request_headers):

    return request_headers[CLIENT_IP]

def get_request_parameters(environ):

    query_string = get_query_string(environ)
    query_params = parse_qs(query_string)

    single_params = {}

    for k in query_params:

        has_more_than_one = (len(query_params[k]) > 1)
        if has_more_than_one:
            single_params[k] = query_params[k]
        else:
            single_params[k] = query_params[k][0]

    return single_params

def get_query_string(environ):

    query_string = environ['QUERY_STRING']

    return query_string

def get_request_body(environ):

    content_length = int(environ['CONTENT_LENGTH'])

    request_body = environ['wsgi.input'].read(content_length)

    request_body_string = request_body.decode(UTF_8)

    request_body_json = json.loads(request_body_string)

    return request_body_json
