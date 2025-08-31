import endpointer.regexp as ep_regexp
from http import HTTPStatus as http_status
import endpointer.api as ep_lambdaf
import endpointer.http as ep_http

SESSION_TOKEN_HEADER = 'com-endpointer-session-token'
SESSION_TOKEN_ENV = 'EP_SESSION_TOKEN'

INVALID_SESSION_TOKEN = 'invalid-session-token'

DOCS_URL = 'https://endpointer.com'

def get_session_token(request_headers):
    
    session_token = request_headers.get(SESSION_TOKEN_HEADER)
    
    no_session_token = session_token is None
    if no_session_token:
        return None
    
    is_invalid = not ep_regexp.is_valid_token(session_token)
    if is_invalid:
        return None
    
    return session_token

def invalid_session_response():

    response_status = http_status.BAD_REQUEST
    response_reason = http_status.BAD_REQUEST.phrase
    response_headers = {}

    response_status_string = f'{response_status} {response_reason}'

    response_body = {

        ep_lambdaf.ERROR_CODE_FIELD:INVALID_SESSION_TOKEN,
        ep_lambdaf.DOCS_URL_FIELD:DOCS_URL

    }

    (response_headers_list, response_body_bytes) = ep_http.prepare_response_package(response_headers, response_body)
    
    return (response_status_string, response_headers_list, response_body_bytes)