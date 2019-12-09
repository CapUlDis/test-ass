import time, logging, json
from datetime import datetime, timedelta
from jwcrypto import jwt, jwk


logger = logging.getLogger(__file__)

def create_token(username, exp, path_token_key):
    try:
        with open(path_token_key, 'r') as f:
            token_key = jwk.JWK.from_json(f.read())
    except FileNotFoundError as err:
        logger.error(f'FileNotFoundError: no credentials.txt in {path_token_key}: {err}')
    except json.decoder.JSONDecodeError as err:
        logger.error(f'JSONDecodeError: data in {path_token_key} is not json: {err}')
        
    token = jwt.JWT(header={"alg": "HS256"},
                    claims={"user": username, "exp": time.mktime((datetime.utcnow() + timedelta(minutes=exp)).timetuple())})
    token.make_signed_token(token_key)
    return token.serialize()

print(create_token('foo', 30, 'token_key.txt'))