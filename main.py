from flask import Flask, request

def create_app():
    app = Flask(__name__)
    return app

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/login', methods=['POST'])
def login():
    
    data = request.get_json(force=True)

    if data['name'] == 'denchik' and data['password'] == 'foobar':
        return 'status = 200 OK'
    else:
        return 'Invalid username/password'
    
if __name__ == '__main__':
    app = create_app()
    app.run()
