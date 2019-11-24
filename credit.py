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
                logger.error('Data in credentials.txt is not dictionary')
                return None
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



        