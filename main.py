import json
from flask import Flask, request, make_response

app = Flask(__name__)

class ContentError(Exception):
    pass
class LogError(Exception):
    pass

@app.route('/login', methods=['POST'])
def login():
    try:
        if request.headers['Content-Type'] == 'application/json':
            data = json.loads(request.get_data())
            if 'name' and 'password' in data.keys():
                if data['name'] == 'denchik' and data['password'] == 'foobar':
                    message = 'OK'
                    http_code = 200
                else:
                    raise LogError
            else: 
                raise ContentError
        else:
            raise ContentError
    except ContentError:
        message = 'BAD REQUEST'
        http_code = 400
    except LogError:
        message = 'FORBIDDEN'
        http_code = 403
        
    return make_response(message, http_code)
    

if __name__ == '__main__':
    app.run()