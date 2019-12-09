import time
from datetime import datetime, timedelta
from jwcrypto import jwt, jwk

    
def create_token(username, exp, path_token_key):

    with open(path_token_key, 'r') as f:
        token_key = jwk.JWK.from_json(f.read())
    
    token = jwt.JWT(header={"alg": "HS256"},
                    claims={"user": username, "exp": time.mktime((datetime.utcnow() + timedelta(minutes=exp)).timetuple())})
    token.make_signed_token(token_key)
    return token.serialize()

print(create_token('foo', 30, 'token_key.txt'))