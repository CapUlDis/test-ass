import json
from flask import Flask, request, make_response

def create_app():
    app = Flask(__name__)
    return app

# if __name__ == '__main__':
app = create_app()
app.run()

@app.route('/login', methods=['POST'])
def login():
    try:
        if request.headers['Content-Type'] != 'application/json':
            message = 'Content-Type not json'
            http_code = 400
            return message, http_code
        
        data = json.loads(request.get_data())
   
    except:
        message = 'Data has not json format'
        http_code = 400
        return message, http_code
    
    else:
        if 'name' not in data.keys() or 'password' not in data.keys():
            message = 'Miss name or/and password'
            http_code = 400
            return message, http_code
        
        if data['name'] == 'denchik' and data['password'] == 'foobar':
            message = 'Correct name and password'
            http_code = 200
            return message, http_code
        else:
            message = 'Wrong name or password'
            http_code = 403
            return message, http_code
