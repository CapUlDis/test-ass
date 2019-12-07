import os, sys, json, logging
from werkzeug.security import generate_password_hash, check_password_hash


logger = logging.getLogger('main.py')

def load_credits(path_credit):
    try:
        with open(path_credit) as f:
            credit = json.load(f)
            if not isinstance(credit, dict):
                logger.error('Data in credentials.txt is not dictionary or malformed')
                raise TypeError
            v = 0
            for value in credit.values():
                if not isinstance(value, str):
                    v += 1
            if v > 0:
                logger.error('TypeError: %d values in credit dictionary are not string' %v)
                raise TypeError
            return credit
    except FileNotFoundError as err:
        logger.error(f'FileNotFoundError: no credentials.txt in {os.path.dirname(os.path.realpath(__file__))}: {err}')
        raise FileNotFoundError
    except json.decoder.JSONDecodeError as err:
        logger.error(f'JSONDecodeError: data in credentials.txt is not json: {err}')
        raise TypeError
    
class Credits:
    
    def __init__(self, path_credit):
        self.load = load_credits(path_credit)
        
    def check_user_with_password_exists(self, name, password):
        if name not in self.load:
            return False
        return check_password_hash(self.load[name], password)

