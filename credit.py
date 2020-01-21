import os, json, logging
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User


logger = logging.getLogger(__file__)


def load_credits(path_credit):
    try:
        with open(path_credit) as f:
            credit = json.load(f)
            if not isinstance(credit, dict):
                logger.error('Data in credentials.txt is not dictionary or malformed.')
                raise TypeError('Data in credentials.txt is not dictionary or malformed.')
            v = 0
            for value in credit.values():
                if not isinstance(value, str):
                    v += 1
            if v > 0:
                logger.error(f'TypeError: {v} values in credit dictionary are not string.')
                raise TypeError(f'TypeError: {v} values in credit dictionary are not string.')
            return credit
    except FileNotFoundError as err:
        logger.error(f'FileNotFoundError: no credentials.txt in {os.path.dirname(os.path.realpath(__file__))}: {err}.')
        raise FileNotFoundError(f'FileNotFoundError: no credentials.txt in {os.path.dirname(os.path.realpath(__file__))}: {err}.')
    except json.decoder.JSONDecodeError as err:
        logger.error(f'JSONDecodeError: data in credentials.txt is not json: {err}.')
        raise TypeError(f'JSONDecodeError: data in credentials.txt is not json: {err}.')
    
class Credits:
    
    def __init__(self, path_credit):
        self.load = load_credits(path_credit)
        
    def check_user_with_password_exists(self, name, password):
        if name not in self.load:
            return False
        return check_password_hash(self.load[name], password)

def check_user_with_password_exists_sqldb(name, password):
    db_session = sessionmaker(bind=create_engine(os.environ.get('TDA_DB'), echo=True))()
    query = db_session.query(User).filter(User.name == name)
    try:
        query.one()
    except NoResultFound as err:
        logger.info(f'NoResultFound: no such username in database: {err}.')
        return False
    except MultipleResultsFound as err:
        logger.error(f'MultipleResultsFound: database has more than one users with such name: {err}.')
        raise LookupError(f'MultipleResultsFound: database has more than one users with such name: {err}.')
    else:
        return check_password_hash(query.one().passwordhash, password)


