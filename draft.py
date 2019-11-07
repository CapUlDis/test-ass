import os, sys
import json
#from main import * 
#from werkzeug.security import generate_password_hash, check_password_hash


'''os.environ['tda_credit'] = '/home/capuldis/repos/to-do-app/credentials.txt'

try:
    with open(os.path.dirname(os.path.realpath(__file__)) + '/credentials.txt') as f:
        credit = json.load(f)
        print(credit['user1'])

except FileNotFoundError:
    print('No such file or working directory')

except json.decoder.JSONDecodeError:
    print('Data in credentials.txt is not json')


print(os.path.realpath(__file__))

print('sys.argv[0] =', sys.argv[0])             
pathname = os.path.dirname(sys.argv[0])        
print('path =', pathname)
print('full path =', os.path.abspath(pathname)) 

print(os.path.dirname(os.path.realpath(__file__)) + '/credentials.txt')'''

def load_credits(path_credit):

    try:
        with open(path_credit) as f:
            credit = json.load(f)
            return credit
    except FileNotFoundError as err:
        print('No such file in working directory:', err)
    except json.decoder.JSONDecodeError as err:
        print('Data in credentials.txt is not json', err)

credit = load_credits(os.path.dirname(os.path.realpath(__file__)) + '/credential.txt')
