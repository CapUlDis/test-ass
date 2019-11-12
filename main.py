import os, json, werkzeug
from flask import Flask, request
from werkzeug.security import generate_password_hash, check_password_hash
from credit import load_credits


credit = load_credits(os.path.dirname(os.path.realpath(__file__)) + '/credentials.txt')

def login():
    
    if type(credit) is not dict:
        return 'Server currently are unavailable.', 500

    try:
        data = request.get_json()
    except werkzeug.exceptions.BadRequest:
        return 'Data is not in json format.', 400
    
    if data is None:
        return 'Content-Type is not json.', 400
        
    if 'name' not in data.keys() or 'password' not in data.keys():
        return 'Name or/and password are missing.', 400
    
    if data['name'] not in credit.keys():
        return 'Such name is not registered.', 403

    if not check_password_hash(credit[data['name']], data['password']):
        return 'Invalid password.', 403
        
    return 'Correct name and password.', 200
    
def create_app():
    app = Flask(__name__)
    app.add_url_rule('/login', view_func=login, methods=['POST'])
    return app

app = create_app()


if __name__ == '__main__':
    app.run()

