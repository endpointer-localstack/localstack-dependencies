import endpointer.regexp as ep_regexp
import endpointer.lambdaf as ep_lambdaf

INVALID_SESSION = 'invalid-session'
DOCS_URL = 'https://docs.endpointer.com/security-no-session'

SESSION_TOKEN_HEADER = 'com-endpointer-session-token'

ACCT_ID = 'acct_id'
SESSION_TOKEN = 'session_token'
REFRESH_TOKEN = 'refresh_token'
CREATED = 'created'
UPDATED = 'updated'
ROLE_OWNER = 1

def check_valid_session_token(request_headers):

    session_token = get_session_token(request_headers)
    has_session_token = session_token is not None
    if not has_session_token:
        raise NoSessionException()
    
def check_valid_session(db_cursor, session_detail):

    has_valid_session = session_detail is not None
    if not has_valid_session:
        raise NoSessionException()

def get_session_detail(db_cursor, session_token):

    sql_param = (session_token, )
    db_cursor.execute(SELECT_SESSION, sql_param)
    row = db_cursor.fetchone()

    row_was_found = row is not None
    if not row_was_found:
        return None
    
    created_str = ep_lambdaf.format_datetime(row['created'])
    updated_str = ep_lambdaf.format_datetime(row['updated'])

    return {

        ACCT_ID:row['acct_id'],
        SESSION_TOKEN:session_token,
        REFRESH_TOKEN:row['refresh_token'],
        CREATED:created_str,
        UPDATED:updated_str

    }

def get_organization_detail(db_cursor, organization_token):

    sql_param = (organization_token, )
    db_cursor.execute(SELECT_SESSION, sql_param)
    row = db_cursor.fetchone()

    row_was_found = row is not None
    if not row_was_found:
        return None
    
    created_str = ep_lambdaf.format_datetime(row['created'])
    updated_str = ep_lambdaf.format_datetime(row['updated'])

    return {

        ACCT_ID:row['acct_id'],
        SESSION_TOKEN:organization_token,
        REFRESH_TOKEN:row['refresh_token'],
        CREATED:created_str,
        UPDATED:updated_str

    }

def get_session_token(request_headers):

    session_token = request_headers.get(SESSION_TOKEN_HEADER)

    has_session_token = session_token is not None
    if not has_session_token:
        return None
    
    has_valid_session_token = ep_regexp.is_valid_token(session_token)

    if not has_valid_session_token:
        return None
    
    return session_token

'''

validate session token
find session record
find organization role
check role
find lambda role

'''

SELECT_SESSION = '''

    select acct_id, refresh_token, created, updated
      from sess_session
        where (session_token = %s)
        
'''

SELECT_ORGANIZATION = '''

    select id
      from orga_organization
        where (organization_token = %s)
        
'''

class NoSessionException(Exception):

    def __init__(self, *args):
        super().__init__(*args)

class NoRequiredRole(Exception):

    def __init__(self, *args):
        super().__init__(*args)
        