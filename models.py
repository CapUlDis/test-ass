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
        return f'<User(name={self.name}, passwordhash={self.passwordhash}, useremail={self.useremail})>'

    def start_engine(self, db_url):
        self.engine = create_engine(db_url)

    def create_table_in_db(self):
        self.__table__.create(bind=self.engine)

    def add_new_user_in_db(self, name, passwordhash, useremail):
        new_user = self.__class__(name=name, passwordhash=passwordhash, useremail=useremail)
        db_session = sessionmaker(bind=self.engine)()
        db_session.add(new_user)
        db_session.commit()

