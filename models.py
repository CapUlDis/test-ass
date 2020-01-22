from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
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

    def create_table_in_db(db_url):
        engine = create_engine(db_url, echo=True)
        Base.metadata.create_all(bind=engine)

    def add_new_user_in_db(self, db_url, name, passwordhash, useremail):
        new_user = self(name=name, passwordhash=passwordhash, useremail=useremail)
        db_session = sessionmaker(bind=create_engine(db_url, echo=True))()
        db_session.add(new_user).commit()

