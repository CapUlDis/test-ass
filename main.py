import json
from flask import Flask, request, make_response


def create_app():
    app = Flask(__name__)
    
    @app.route('/login', methods=['POST'])
    def login():
        
        if 'Content-Type' not in request.headers.keys() or request.headers['Content-Type'] != 'application/json':
            http_code = 400
            return 'Content-Type is not json.', http_code
            
        try:    
            data = json.loads(request.get_data())
        except json.decoder.JSONDecodeError:
            http_code = 400
            return 'Data is not in json format.', http_code
                
        if 'name' not in data.keys() or 'password' not in data.keys():
            http_code = 400
            return 'Name or/and password are missing.', http_code
        
        if data['name'] == 'denchik' and data['password'] == 'foobar':
            http_code = 200
            return 'Correct name and password.', http_code
        else:
            http_code = 403
            return 'Wrong name or password.', http_code

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()

