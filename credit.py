import os, sys, logging
import json
from werkzeug.security import generate_password_hash, check_password_hash


logging.basicConfig(filename="main.log", 
                    format='%(asctime)s %(message)s', 
                    filemode='w') 
logger = logging.getLogger() 
logger.setLevel(logging.ERROR) 

def load_credits(path_credit):

    try:
        with open(path_credit) as f:
            credit = json.load(f)
            if type(credit) is not dict:
                return None
            return credit
    except FileNotFoundError as err:
        logger.error(f'FileNotFoundError: no credentials.txt in {os.path.dirname(os.path.realpath(__file__))}: {err}')
        return None
    except json.decoder.JSONDecodeError as err:
        logger.error(f'JSONDecodeError: data in credentials.txt is not json: {err}')
        return None

def valid_user(pwhash, password):

    if check_password_hash(pwhash, password):
        return True
    return False