import os, werkzeug, logging
from flask import Flask, request, current_app, jsonify
from credit import Credits
from auth import TokenGenerator


logging.basicConfig(filename="main.log", 
                    format='%(asctime)s %(message)s', 
                    filemode='w',
                    level = logging.INFO) 
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
        
    return jsonify({'token': current_app.token_gen.create_new_token(data['name'], current_app.token_exp)}), 200

def return_user_workspace():
    
    try:
        token = request.headers['Authorization']
    except KeyError as inf:
        logger.info(f'In post request Authorization header missing: {inf}')
        return 'Please log in again', 401
    
    token = token.replace('Bearer ', '')

    if token == '':
        logger.info('In Authorization header token missing')
        return 'Please log in again', 401

    if not current_app.token_gen.check_token(token):
        logger.info('Got invalid token')
        return 'Please log in again', 401

    return jsonify({
        'userName': 'denchik',
        'id': 1,
        'numOfLists': 1,
        'toDoLists': {
            'listName': 'First to-do list',
            'listDate': '19 Dec 2019',
            'listColor': 'green',
            'listItems': [
                {
                    'itemNum': 1,
                    'itemName': 'Buy some milk',
                    'itemDeadline': 'today',
                    'checkBox': False,
                },
                {
                    'itemNum': 2,
                    'itemName': 'Clean apartment',
                    'itemDeadline': None,
                    'checkBox': False,
                },
                {
                    'itemNum': 3,
                    'itemName': 'Read about Flask framework',
                    'itemDeadline': '20 Dec 2019 11:00 AM',
                    'checkBox': True,
                }
                        ],
            'listTags': ['general', 'daily']
                    }

    }), 200

def create_app():
    app = Flask(__name__)
    app.add_url_rule('/login', view_func=login, methods=['POST'])
    app.add_url_rule('/my-todos', view_func=return_user_workspace, methods=['POST'])
    app.credit = Credits(os.environ.get('TDA_CREDITS'))
    app.token_gen = TokenGenerator(os.environ.get('TDA_TOKEN_KEY'))
    app.token_exp = int(os.environ.get('TDA_TOKEN_EXPIRATION_MINUTES'))
    return app


if __name__ == '__main__':
    app = create_app()
    app.run()


