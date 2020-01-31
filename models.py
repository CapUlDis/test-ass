from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    passwordhash = Column(String, nullable=False)
    useremail = Column(String, nullable=False)

    def __repr__(self):
        return f'<User(name={self.name}, passwordhash={self.passwordhash}, useremail={self.useremail})>'

  