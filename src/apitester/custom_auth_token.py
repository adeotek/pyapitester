import hashlib
from datetime import datetime, timedelta


def generate_token(secret_key: str, client_id: str = '', server_id: str = '', validity: int = 10):
    if secret_key == '':
        raise ValueError('Invalid `secretKey`')
    token_source = 'Sk:' + secret_key + '-Iss:' + server_id
    token = hashlib.sha256(token_source.encode('ascii')).hexdigest()
    expires_at = datetime.now() + timedelta(minutes=validity)
    expires_at_token = expires_at.strftime('%Y-%m-%dT%H:%M:%S').encode('ascii').hex().lower()
    return client_id + token + expires_at_token, expires_at


def validate_token(token, secret_key: str, server_id: str = ''):
    if not isinstance(token, str) or token == '' or len(token) < 102:
        return False, None, 'Invalid token value/size!'
    if not isinstance(secret_key, str) or secret_key == '':
        return False, None, 'Invalid `secretKey` value!'
    client_id = token[0:-102]
    token_source = 'Sk:' + secret_key + '-Iss:' + server_id
    check_hash = hashlib.sha256(token_source.encode('ascii')).hexdigest()
    token_hash = token[-102:-38]
    if check_hash.lower() != token_hash.lower():
        return False, client_id, 'Invalid token!'
    exp_date = datetime.strptime(bytes.fromhex(token[-38:]).decode(), '%Y-%m-%dT%H:%M:%S')
    if exp_date > datetime.now():
        return True, client_id, ''
    else:
        return False, client_id, 'Token has expired!'
