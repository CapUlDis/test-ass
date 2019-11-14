import os, json, werkzeug
from flask import Flask, request
from credit import load_credits, valid_user


def login():
    
    try:
        data = request.get_json()
    except werkzeug.exceptions.BadRequest:
        return 'Data is not in json format.', 400
    
    if data is None:
        return 'Content-Type is not json.', 400
        
    if 'name' not in data or 'password' not in data:
        return 'Name or/and password are missing.', 400
    
    credit = load_credits(os.path.dirname(os.path.realpath(__file__)) + '/credentials.txt')
    if credit == None:
        return 'Server currently are unavailable.', 500

    if data['name'] not in credit:
        return 'Invalid name or password.', 403

    if not valid_user(credit[data['name']], data['password']):
        return 'Invalid name or password.', 403
        
    return 'Correct name and password.', 200
    
def create_app():
    app = Flask(__name__)
    app.add_url_rule('/login', view_func=login, methods=['POST'])
    return app
app = create_app()


if __name__ == '__main__':
    app.run()

