from io import StringIO
import random
import string
import time
import tokenize

DEFAULT_LENGHT = 15

WHITELIST_IMPORTS = [

    'endpointer', 'datetime', 'decimal', 'json', 'contextlib', 'itertools',
    'mysql.connector', 'requests'

]

WHITELIST_FUNCTIONS = [

    'abs', 'all', 'any', 'bin', 'bool', 'callable', 'chr', 'complex', 'dict',
    'enumerate', 'filter', 'float', 'format', 'frozenset', 'getattr', 'hasattr',
    'hash', 'hex', 'id', 'int', 'isinstance', 'issubclass', 'iter', 'len', 'list',
    'map', 'max', 'min', 'next', 'object', 'oct', 'ord', 'pow', 'print', 'range',
    'repr', 'round', 'set', 'slice', 'sorted', 'str', 'sum', 'tuple', 'type', 'zip'

]

WHITELIST_TYPES = [

    'int', 'float', 'bool', 'str', 'list', 'tuple', 'dict', 'set', 'frozenset',
    'complex', 'bytes', 'bytearray', 'memoryview', 'range', 'type', 'object',
    'Exception', 'BaseException', 'ValueError', 'KeyError', 'IndexError',
    'AttributeError', 'RuntimeError', 'StopIteration',
    'NotImplementedType', 'NoneType'

]

python_code = """

eval('print("Hello, World!")')
import os
import requests
with open('aaa') as f:
    f.write('bbb')
len((a, b, c))
aaa = ''

"""

def whitelist(content):

    code_reader = StringIO(content)

    # Generate tokens from the code
    tokens = tokenize.generate_tokens(code_reader.readline)

    # Iterate through the tokens and print their information
    # for (type, name, *rest) in tokens:
    #     print((type, name))
    # for token in tokens:
    #     print(token)

    is_import = False

    for token in tokens:

        if token.type != 1:

            continue
        
        if is_import:
            
            is_allowed_import = token.string in WHITELIST_IMPORTS or token.string.startswith('endpointer')
            
            if not is_allowed_import:
                print('Illegal import = ' + token.string)
            else:
                print('Legal import = ' + token.string)
            
            is_import = False

            continue

        is_import = (token.string == 'import')
        
        if is_import:
            continue

        is_open_parenthesis = (next(tokens).string == '(')
        
        if is_open_parenthesis:
            print(token.string)
            is_legal_token = token.string in WHITELIST_FUNCTIONS

            if not is_legal_token:

                print('Illegal token = ' + token.string)

            else:
                
                print('Legal token = ' + token.string)

whitelist(python_code)

def generate_unique_token(db_cursor, token_select):

    token = generate_token()

    tokens_exists = check_token_exists(db_cursor, token_select, token)
    while tokens_exists:

        time.sleep(200/1000)
        token = generate_token()
        tokens_exists = check_token_exists(db_cursor, token_select, token)

    return token

def check_token_exists(db_cursor, token_select, token):

    sql_param = (token, )
    db_cursor.execute(token_select, sql_param)
    (row_count,) = db_cursor.fetchone()
    
    return (row_count != 0)

def generate_token(length=DEFAULT_LENGHT):

    characters = string.ascii_letters + string.digits  # a-zA-Z0-9
    token = ''.join(random.choices(characters, k=length))
    return token

