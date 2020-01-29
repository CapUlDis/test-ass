from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from flask import current_app


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    passwordhash = Column(String, nullable=False)
    useremail = Column(String, nullable=False)

    def __repr__(self):
        return f'<User(name={self.name}, passwordhash={self.passwordhash}, useremail={self.useremail})>'

    def add_new_user_in_db(self, name, passwordhash, useremail):
        new_user = self.__clasls__(name=name, passwordhash=passwordhash, useremail=useremail)
        db_session = current_app.Session()
        db_session.add(new_user)
        db_session.commit()

