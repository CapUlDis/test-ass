import os, sys, logging
import json


logging.basicConfig(filename="main.log", 
                    format='%(asctime)s %(message)s', 
                    filemode='w') 
logger = logging.getLogger() 
logger.setLevel(logging.ERROR) 

def load_credits(path_credit):

    try:
        with open(path_credit) as f:
            credit = json.load(f)
            return credit
    except FileNotFoundError as err:
        logger.error(f'FileNotFoundError: no credentials.txt in {os.path.dirname(os.path.realpath(__file__))}')
    except json.decoder.JSONDecodeError as err:
        logger.error(f'JSONDecodeError: data in credentials.txt is not json')

