import os, werkzeug, logging
from flask import Flask, request, current_app, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from credit import check_user_with_password_exists, check_useremail_exist, generate_password, add_new_user_to_db
from auth import TokenGenerator


logging.basicConfig(filename="main.log", 
                    format='%(asctime)s %(message)s', 
                    filemode='w',
                    level = logging.INFO) 
logger = logging.getLogger() 


def login():
    
    try:
        data = request.get_json()
    except werkzeug.exceptions.BadRequest as inf:
        logger.info(f'Received data is not in json format: {inf}')
        return 'Data is not in json format.', 400
    
    if data is None:
        logger.info('In POST request Content-Type header is not json.')
        return 'Content-Type is not json.', 400
        
    if 'name' not in data or 'password' not in data:
        logger.info('In POST request name or/and password are missing.')
        return 'Name or/and password are missing.', 400

    if not isinstance(data['name'], str):
        logger.info('In POST request name is not a string.')
        return 'Name is not a string.', 400

    if not isinstance(data['password'], str):
        logger.info('In POST request password is not a string.')
        return 'Password is not a string.', 400

    if not check_user_with_password_exists(data['name'], data['password']):
        logger.info('In POST request name or password is invalid.')
        return 'Invalid name or password.', 403
        
    return jsonify({'token': current_app.token_gen.create_new_token(data['name'], current_app.token_exp)}), 200

def return_user_workspace():
    
    try:
        token = request.headers['Authorization']
    except KeyError as inf:
        logger.info(f'In POST request Authorization header is missing: {inf}.')
        return 'In POST request Authorization header is missing.', 401
    
    token = token.replace('Bearer ', '')

    if token == '':
        logger.info('In Authorization header token is missing.')
        return 'In Authorization header token is missing.', 401

    if not current_app.token_gen.check_token(token):
        logger.info('Got invalid token.')
        return 'Please log in again.', 401

    return jsonify({
        'userName': 'denchik',
        'id': 1,
        'toDoLists': {
            'listName': 'First to-do list',
            'creationDate': '19 Dec 2019',
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

def register_user():

    try:
        data = request.get_json()
    except werkzeug.exceptions.BadRequest as inf:
        logger.info(f'Received data is not in json format: {inf}')
        return 'Data is not in json format.', 400
    
    if data is None:
        logger.info('In POST request Content-Type header is not json.')
        return 'Content-Type is not json.', 400
        
    if 'name' not in data or 'useremail' not in data:
        logger.info('In POST request name or/and useremail are missing.')
        return 'Name or/and useremail are missing.', 400

    if not isinstance(data['name'], str):
        logger.info('In POST request name is not a string.')
        return 'Name is not a string.', 400

    if not isinstance(data['useremail'], str):
        logger.info('In POST request useremail is not a string.')
        return 'Useremail is not a string.', 400

    if check_useremail_exist(data['useremail']):
        logger.info('POST request useremail already exists in database.')
        return 'User with such email is already registered.', 400
    
    new_password = generate_password()
    add_new_user_to_db(data['name'], new_password, data['useremail'])

    return jsonify({'newPassword': new_password, 'token': current_app.token_gen.create_new_token(data['name'], current_app.token_exp)}), 200

def create_app():
    app = Flask(__name__)
    app.engine = create_engine(os.environ.get('TDA_DB'), echo=True)
    app.Session = sessionmaker(bind=app.engine)
    app.add_url_rule('/login', view_func=login, methods=['POST'])
    app.add_url_rule('/my-todos', view_func=return_user_workspace, methods=['POST'])
    app.add_url_rule('/register', view_func=register_user, methods=['POST'])
    app.token_gen = TokenGenerator(os.environ.get('TDA_TOKEN_KEY'))
    app.token_exp = int(os.environ.get('TDA_TOKEN_EXPIRATION_MINUTES'))
    return app


if __name__ == '__main__':
    app = create_app()
    app.run()


