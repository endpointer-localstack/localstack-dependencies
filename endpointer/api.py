import endpointer.http as ep_http
from http import HTTPStatus as http_status

RESOURCE_REFERENCE_FIELD = 'resource-reference'
RESOURCE_TOKEN_FIELD = 'resource-token'
RESOURCE_ALIAS_FIELD = 'resource-alias'

ERROR_CODE_FIELD = 'error-code'
DOCS_URL_FIELD = 'docs-url'

PATCH_OP = 'op'

INVALID_RESOURCE_REFERENCE = 'invalid-resource-reference'
INVALID_RESOURCE_TOKEN = 'invalid-resource-token'
RESOURCE_NOT_DEPLOYED = 'resource-not-deployed'
INVALID_JSON_BODY = 'invalid-json-body'

DOCS_URL = 'https://docs.endpointer.com/security-no-session'

FORMAT_DATETIME = '%Y-%m-%d %H:%M:%S'

def format_datetime(date_time, format_string=FORMAT_DATETIME):

    date_time_string = date_time.strftime('%Y-%m-%d %H:%M:%S')
    return date_time_string

def get_resource_token(request_uri):

    resource_token = request_uri[0]

    return resource_token

def get_api_token(request_uri):

    api_token = request_uri[0]

    return api_token

def get_lambda_token(request_parameters):

    lambda_reference = get_lambda_reference(request_parameters)

    lambda_token = lambda_reference.split('.')[1]

    return lambda_token

def get_lambda_reference(request_parameters):
    
    lambda_reference = request_parameters.get(RESOURCE_REFERENCE_FIELD)

    return lambda_reference

def has_valid_lambda_reference(request_parameters):

    lambda_reference = request_parameters.get(RESOURCE_REFERENCE_FIELD)
    not_found = lambda_reference is None
    if not_found:
        return False
    
    return True

def has_valid_lambda_token(request_parameters):

    lambda_token = request_parameters.get(RESOURCE_TOKEN_FIELD)
    has_lambda_token = lambda_token is not None
    if not has_lambda_token:
        return False
    
    # restore when resource deployed
    # has_valid_lambda_token = ep_regexp.is_valid_token(lambda_token[0])
    # if not has_valid_lambda_token:
    #     return False
    
    return True

def ok_response(response_headers, response_body):

    return {

        ep_http.RESPONSE_STATUS: http_status.OK,
        ep_http.RESPONSE_HEADERS: response_headers,
        ep_http.RESPONSE_BODY: response_body

    }

def created_response(response_headers, response_body):

    return {

        ep_http.RESPONSE_STATUS: http_status.CREATED,
        ep_http.RESPONSE_HEADERS: response_headers,
        ep_http.RESPONSE_BODY: response_body

    }

def no_content_response(response_headers):

    response_body = {}

    return {

        ep_http.RESPONSE_STATUS: http_status.NO_CONTENT,
        ep_http.RESPONSE_HEADERS: response_headers,
        ep_http.RESPONSE_BODY: response_body

    }

def not_found_response(response_headers):

    response_body = {}

    return {

        ep_http.RESPONSE_STATUS: http_status.NOT_FOUND,
        ep_http.RESPONSE_HEADERS: response_headers,
        ep_http.RESPONSE_BODY: response_body

    }

def bad_request_response(response_headers, error_code, docs_url):

    return send_error(http_status.BAD_REQUEST, response_headers, error_code, docs_url)

def unauthorized_response(response_headers, error_code, docs_url):

    return send_error(http_status.UNAUTHORIZED, response_headers, error_code, docs_url)

def send_error(response_status, response_headers, error_code, docs_url):

    response_body = {

        ERROR_CODE_FIELD:error_code,
        DOCS_URL:docs_url

    }

    return {

        ep_http.RESPONSE_STATUS: response_status,
        ep_http.RESPONSE_HEADERS: response_headers,
        ep_http.RESPONSE_BODY: response_body

    }

def lambda_not_found_response():

    response_headers = {}

    return bad_request_response(response_headers, INVALID_RESOURCE_TOKEN, DOCS_URL)
