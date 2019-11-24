import os, json, werkzeug
from flask import Flask, request, current_app
from credit import Credits



def login():
    
    try:
        data = request.get_json()
    except werkzeug.exceptions.BadRequest:
        return 'Data is not in json format.', 400
    
    if data is None:
        return 'Content-Type is not json.', 400
        
    if 'name' not in data or 'password' not in data:
        return 'Name or/and password are missing.', 400
    
    if not current_app.credit.check_name(data['name']):
        return 'Invalid name or password.', 403

    if not current_app.credit.check_pass(data['name'], data['password']):
        return 'Invalid name or password.', 403
        
    return 'Correct name and password.', 200
    
def create_app():
    app = Flask(__name__)
    app.add_url_rule('/login', view_func=login, methods=['POST'])
    app.credit = Credits(os.environ.get('todoappcredits'))
    return app


if __name__ == '__main__':
    app = create_app()
    app.run()

