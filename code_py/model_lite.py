from sqlalchemy import Column, String, Integer, create_engine, ForeignKeyConstraint, Sequence, TIMESTAMP, Text, \
    ForeignKey, Date, BLOB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, scoped_session, sessionmaker
from sqlalchemy_utils import PhoneNumber

# from code_py.settings import settings
import logging

logger = logging.getLogger(__name__)

engine = create_engine('sqlite:///mybase_lite.db')
db_session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()




class Gamer(Base):
    __tablename__ = 'gamer'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(120))
    last_name = Column(String(120))
    nick_name = Column(String(120))
    chat_id = Column(Integer)
    # TODO сделать класс с проверкой на номер
    gamer_phone = Column(String(120))
    gamer_email = Column(String(120))

    def __init__(self, id=None, first_name=None, last_name=None, nick_name=None, chat_id=None, gamer_phone=None,
                 gamer_email=None, teamanswer=None, team=None, gamer_x_game=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.nick_name = nick_name
        self.chat_id = chat_id
        self.gamer_phone = gamer_phone
        self.gamer_email = gamer_email
        self.teamanswer = teamanswer
        self.team = team
        self.gamer_x_game = gamer_x_game

class Team_x_Gamer(Base):
    __tablename__ = 'team_x_gamer'
    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('team.id'))
    gamer_id = Column(Integer, ForeignKey('gamer.id'))

    def __init__(self, id=None, team_id=None, gamer_id=None):
        self.id = id
        self.team_id = team_id
        self.gamer_id = gamer_id

if __name__ == "__main__":
    print ('olol')
    Base.metadata.create_all(bind=engine)
