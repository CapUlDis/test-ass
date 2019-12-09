import datetime
from jwcrypto import jwt, jwk


token_key = jwk.JWK(generate='oct', size=256)

token = jwt.JWT(header={"alg": "HS256"},
                claims={"user": data['name'], "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)})
token.make_signed_token(token_key)