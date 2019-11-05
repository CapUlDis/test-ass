import os
import json
#from werkzeug.security import generate_password_hash, check_password_hash


os.environ['tda_credit'] = '/home/capuldis/repos/to-do-app/credentials.txt'

try:
    with open(os.environ['tda_credit']) as f:
        credit = json.load(f)
        print(credit['user1'])

except FileNotFoundError:
    print('No such file or working directory')

except json.decoder.JSONDecodeError:
    print('Data in credentials.txt is not json')
