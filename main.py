import os, json, werkzeug
import logging 
from flask import Flask, request
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
            return credit
    except FileNotFoundError:
        logger.error('FileNotFoundError: no credentials.txt in ' + os.path.dirname(os.path.realpath(__file__)))
    except json.decoder.JSONDecodeError:
        logger.error('JSONDecodeError: data in credentials.txt is not json')

def login():
  
    try:
        data = request.get_json()
    except werkzeug.exceptions.BadRequest:
        return 'Data is not in json format.', 400
    
    if data is None:
        return 'Content-Type is not json.', 400
        
    if 'name' not in data.keys() or 'password' not in data.keys():
        return 'Name or/and password are missing.', 400
    
    if data['name'] == 'denchik' and data['password'] == 'foobar':
        return 'Correct name and password.', 200
    
    return 'Wrong name or password.', 403
    
def create_app():
    app = Flask(__name__)
    app.add_url_rule('/login', view_func=login, methods=['POST'])
    return app

app = create_app()


if __name__ == '__main__':
    app.run()

