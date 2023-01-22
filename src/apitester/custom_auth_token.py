import hashlib
from datetime import datetime, timedelta


def generate_token(secretKey: str, clientId: str = '', serverId: str = '', validity: int = 10):
    if secretKey == '':
        raise ValueError('Invalid `secretKey`')
    tokenSource = 'Sk:' + secretKey + '-Iss:' + serverId
    token = hashlib.sha256(tokenSource.encode('ascii')).hexdigest()
    expiresAt = datetime.now() + timedelta(minutes=validity)
    expiresAtToken = expiresAt.strftime('%Y-%m-%dT%H:%M:%S').encode('ascii').hex().lower()
    return clientId + token + expiresAtToken, expiresAt


def validate_token(token, secretKey: str, serverId: str = ''):
    if not isinstance(token, str) or token == '' or len(token) < 102:
        return False, None, 'Invalid token value/size!'
    if not isinstance(secretKey, str) or secretKey == '':
        return False, None, 'Invalid `secretKey` value!'
    clientId = token[0:-102]
    tokenSource = 'Sk:' + secretKey + '-Iss:' + serverId
    checkHash = hashlib.sha256(tokenSource.encode('ascii')).hexdigest()
    tokenHash = token[-102:-38]
    if checkHash.lower() != tokenHash.lower():
        return False, clientId, 'Invalid token!'
    expDate = datetime.strptime(bytes.fromhex(token[-38:]).decode(), '%Y-%m-%dT%H:%M:%S')
    if expDate > datetime.now():
        return True, clientId, ''
    else:
        return False, clientId, 'Token has expired!'
