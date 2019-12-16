import os, werkzeug, logging
from flask import Flask, request, current_app, jsonify
from credit import Credits
from auth import Token_gen


logging.basicConfig(filename="main.log", 
                    format='%(asctime)s %(message)s', 
                    filemode='w',
                    level = logging.WARNING) 
logger = logging.getLogger() 

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
        return 'Name is not a string.', 400

    if not isinstance(data['password'], str):
        return 'Password is not a string.', 400

    if not current_app.credit.check_user_with_password_exists(data['name'], data['password']):
        return 'Invalid name or password.', 403
        
    return jsonify({'token': current_app.token.create_new_token(data['name'], current_app.token_exp)}), 200
    
def create_app():
    app = Flask(__name__)
    app.add_url_rule('/login', view_func=login, methods=['POST'])
    app.credit = Credits(os.environ.get('tda_credits'))
    app.token = Token_gen(os.environ.get('tda_token_key'))
    app.token_exp = 30
    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
