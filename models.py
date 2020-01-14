from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    passwordhash = Column(String)
    useremail = Column(String)

    def __repr__(self):
       return "<User(name='%s', passwordhash='%s', useremail='%s')>" % (
                            self.name, self.passwordhash, self.useremail)

