import os, json, werkzeug
from flask import Flask, request, current_app
from credit import Credits, logger


def login():
    
    try:
        data = request.get_json()
    except werkzeug.exceptions.BadRequest:
        return 'Data is not in json format.', 400
    
    if data is None:
        return 'Content-Type is not json.', 400
        
    if 'name' not in data or 'password' not in data:
        return 'Name or/and password are missing.', 400

    if not isinstance(data['name'], str):
        data['name'] = str(data['name'])
        logger.warning('WARNING: Client sent not string name')

    if not isinstance(data['password'], str):
        data['password'] = str(data['password'])
        logger.warning('WARNING: Client sent not string password')

    if not current_app.credit.check_user_with_password_exists(data['name'], data['password']):
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

