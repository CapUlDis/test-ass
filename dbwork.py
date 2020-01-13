from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String


engine = create_engine('postgresql://test_1:foobar@localhost/test_1', echo=True)

Base = declarative_base()

Session = sessionmaker(bind=engine)

session = Session()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)

    def __repr__(self):
       return "<User(name='%s', fullname='%s', nickname='%s')>" % (
                            self.name, self.fullname, self.nickname)

Base.metadata.create_all(engine)


'''ed_user = User(name='ed', fullname='Ed Jones', nickname='edsnickname')

session.add(ed_user)

session.commit()'''

session.add_all([
    User(name='wendy', fullname='Wendy Williams', nickname='windy'),
    User(name='mary', fullname='Mary Contrary', nickname='mary'),
    User(name='fred', fullname='Fred Flintstone', nickname='freddy')])

session.commit()