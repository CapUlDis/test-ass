import logging
from werkzeug.security import check_password_hash
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from flask import current_app
from models import User


logger = logging.getLogger(__file__)


def check_user_with_password_exists(name, password):
    db_session = current_app.Session()
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


