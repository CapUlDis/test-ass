from flask import Flask, request
from flask_json import FlaskJSON

app = Flask(__name__)
FlaskJSON(app)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()

@app.route('/login', methods=['POST'])
def login():
    
    data = request.get_json(force=True)

    if data['name'] == 'denchik' and data['password'] == 'foobar':
        return 'status = 200 OK'
    else:
        return 'Invalid username/password'
    
if __name__ == '__main__':
    app.run()