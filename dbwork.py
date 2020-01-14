from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    Name = Column(String)
    Passwordhash = Column(String)
    Useremail = Column(String)

    def __repr__(self):
       return "<User(Name='%s', Passwordhash='%s', Useremail='%s')>" % (
                            self.Name, self.Passwordhash, self.Useremail)

