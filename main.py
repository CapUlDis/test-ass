import os, json, werkzeug
from flask import Flask, request
from credit import Credits


credit = Credits('/home/capuldis/repos/to-do-app/credentials.txt')

def login():
    
    try:
        data = request.get_json()
    except werkzeug.exceptions.BadRequest:
        return 'Data is not in json format.', 400
    
    if data is None:
        return 'Content-Type is not json.', 400
        
    if 'name' not in data or 'password' not in data:
        return 'Name or/and password are missing.', 400
    
    if not credit.check_name(data['name']):
        return 'Invalid name or password.', 403

    if not credit.check_pass(data['name'], data['password']):
        return 'Invalid name or password.', 403
        
    return 'Correct name and password.', 200
    
def create_app():
    app = Flask(__name__)
    app.add_url_rule('/login', view_func=login, methods=['POST'])
    return app

if credit != None:   
    app = create_app()


if __name__ == '__main__':
    app.run()

