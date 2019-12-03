import os, sys, json
from main import logger
from werkzeug.security import generate_password_hash, check_password_hash


def load_credits(path_credit):

    try:
        with open(path_credit) as f:
            credit = json.load(f)
            if not isinstance(credit, dict):
                logger.error('Data in credentials.txt is not dictionary')
                raise TypeError
            k = 0
            v = 0
            for key in credit:
                if not isinstance(key, str):
                    k += 1
            for value in credit:
                if not isinstance(value, str):
                    v += 1
            if k > 0 or v > 0:
                logger.error(TypeError('%d keys and %d values in credit dictionary are not string' % (k, v)))
                raise TypeError
            return credit
    except FileNotFoundError as err:
        logger.error(f'FileNotFoundError: no credentials.txt in {os.path.dirname(os.path.realpath(__file__))}: {err}')
        return None
    except json.decoder.JSONDecodeError as err:
        logger.error(f'JSONDecodeError: data in credentials.txt is not json: {err}')
        return None

class Credits:
    
    def __init__(self, path_credit):
        self.load = load_credits(path_credit)
        
    def check_user_with_password_exists(self, name, password):
        if name not in self.load:
            return False
        return check_password_hash(self.load[name], password)
