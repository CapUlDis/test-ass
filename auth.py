import calendar, logging, json
from datetime import datetime, timedelta
from jwcrypto import jwt, jwk, jws


logger = logging.getLogger(__file__)

def load_token_key(path_token_key):
    try:
        with open(path_token_key, 'r') as f:
            token_key = jwk.JWK.from_json(f.read())
            return token_key
    except FileNotFoundError as err:
        logger.error(f'FileNotFoundError: no credentials.txt in {path_token_key}: {err}')
        raise FileNotFoundError(f'FileNotFoundError: no credentials.txt in {path_token_key}: {err}')
    except jwk.InvalidJWKValue as err:
        logger.error(f'InvalidJWKValue: data in {path_token_key} is not JWK object')     
        raise TypeError(f'InvalidJWKValue: data in {path_token_key} is not JWK object')   
    
class Token_gen:

    def __init__(self, path_token_key):
        self.load_key = load_token_key(path_token_key)

    def create_new_token(self, username, token_exp):
        token = jwt.JWT(header={"alg": "HS256"},
                        claims={"user": username, "exp": calendar.timegm((datetime.utcnow() + timedelta(minutes = token_exp)).timetuple())})
        token.make_signed_token(self.load_key)
        return token.serialize()

    def check_token(self, token):
        try:
            jwt.JWT(key = self.load_key, jwt = token)
            return True
        except jwt.JWTExpired as inf:
            logger.info(f'JWTExpired: token is expired: {inf}')
            return False
        except jws.InvalidJWSSignature as inf:
            logger.info(f'InvalidJWSSignature: token has invalid signature: {inf}')
            return False
        except jws.InvalidJWSObject as inf:
            logger.info(f'InvalidJWSObject: invalid token format: {inf}')
            return False
        except ValueError as inf:
            logger.info(f'ValueError: received string is not JSON Web Token: {inf}')
            return False
        


