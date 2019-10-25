import json
import werkzeug
import sys
from flask import Flask, request


def create_app():
    app = Flask(__name__)
    return app

app = create_app()

@app.route('/login', methods=['POST'])
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

if __name__ == '__main__':
    app.run()



