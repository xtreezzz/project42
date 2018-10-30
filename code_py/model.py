from sqlalchemy import Column, String, Integer, create_engine, ForeignKeyConstraint, Sequence, TIMESTAMP, Text, \
    ForeignKey, Date, BLOB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, scoped_session, sessionmaker
from sqlalchemy_utils import PhoneNumber

# from code_py.settings import settings
import logging

logger = logging.getLogger(__name__)

engine = create_engine('sqlite:///mybase.db')
db_session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


class GameWeek(Base):
    __tablename__ = 'game_week'
    id = Column(Integer, primary_key=True)
    name_id = Column(Integer)
    start_date = Column(Date)
    end_date = Column(Date)
    is_special = Column(Integer, server_default='0')
    week_desc = Column(String(512))

    game = relationship("Game", back_populates="gameweek")

    def __init__(self, id=None, name_id=None, start_date=None, end_date=None, is_special=None, week_desc=None):
        self.id = id
        self.name_id = name_id
        self.start_date = start_date
        self.end_date = end_date
        self.is_special = is_special
        self.week_desc = week_desc
        # self.game = game


class Game(Base):
    __tablename__ = 'game'
    id = Column(Integer, primary_key=True)
    game_week_id = Column(Integer, ForeignKey('game_week.id'))
    name_id = Column(Integer)
    week_desc = Column(String(512))
    game_date = Column(Date)

    gameweek = relationship("GameWeek", back_populates="game")
    gametour = relationship("GameTour", back_populates="game")
    team = relationship("Team", back_populates="game", secondary='team_x_game')
    #gamer_x_game = relationship("Gamer", back_populates="game", secondary='Game_x_Gamer_Team')

    def __init__(self, id=None, game_week_id=None, name_id=None, week_desc=None, game_date=None):
        self.id = id
        self.game_week_id = game_week_id
        self.name_id = name_id
        self.week_desc = week_desc
        self.game_date = game_date
        # self.gameweek = gameweek
        # self.gametour = gametour
        # self.team = team
        # self.gamer_x_game = gamer_x_game


class GameTour(Base):
    __tablename__ = 'game_tour'
    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('game.id'))
    tour_type = Column(String(25))
    tour_index = Column(Integer)
    game = relationship("Game", back_populates="gametour")
    tourquestion = relationship("TourQuestion", back_populates="gametour")

    def __init__(self, id=None, game_id=None, tour_type=None, tour_index=None, game=None, tourquestion=None):
        self.id = id
        self.game_id = game_id
        self.tour_type = tour_type
        self.tour_index = tour_index
        # self.game = game
        # self.tourquestion = tourquestion


class TourQuestion(Base):
    __tablename__ = 'tour_question'
    id = Column(Integer, primary_key=True)
    game_tour_id = Column(Integer, ForeignKey('game_tour.id'))
    question_id = Column(Integer, ForeignKey('question.id'))
    question_index = Column(Integer)
    posted_dttm = Column(TIMESTAMP)

    gametour = relationship("GameTour", back_populates="tourquestion")
    question = relationship("Question", back_populates="tourquestion")
    teamanswer = relationship("TeamAnswer", back_populates="tourquestion")

    def __init__(self, id=None, game_tour_id=None, question_id=None, question_index=None, posted_dttm=None,
                 gametour=None, question=None, teamanswer=None):
        self.id = id
        self.game_tour_id = game_tour_id
        self.question_id = question_id
        self.question_index = question_index
        self.posted_dttm = posted_dttm
        # self.gametour = gametour
        # self.question = question
        # self.teamanswer = teamanswer


class Question(Base):
    __tablename__ = 'question'
    id = Column(Integer, primary_key=True)
    question_type = Column(String(25))
    question_content = Column(BLOB)
    question_prompt_type = Column(String(25))
    question_prompt = Column(String(512))
    question_answer = Column(BLOB)

    tourquestion = relationship("TourQuestion", back_populates="question")
    # teamanswer = relationship("TeamAnswer", back_populates="question")

    def __init__(self, id=None, question_type=None, question_content=None, question_prompt_type=None,
                 question_prompt=None, question_answer=None, tourquestion=None, teamanswer=None):
        self.id = id
        self.question_type = question_type
        self.question_content = question_content
        self.question_prompt_type = question_prompt_type
        self.question_prompt = question_prompt
        self.question_answer = question_answer
        # self.tourquestion = tourquestion
        # self.teamanswer = teamanswer


class TeamAnswer(Base):
    __tablename__ = 'team_answer'
    id = Column(Integer, primary_key=True)
    answer = Column(BLOB)
    is_correct = Column(Integer)
    is_recognized = Column(Integer)
    team_id = Column(Integer, ForeignKey('team.id'))
    gamer_id = Column(Integer, ForeignKey('gamer.id'))
    question_id = Column(Integer, ForeignKey('tour_question.id'))

    # game_id = Column(Integer, ForeignKey('tour_question.id'))
    # question_id = Column(Integer, ForeignKey('question.id'))
    answer_dttm = Column(TIMESTAMP)

    # question = relationship("Question", back_populates="team_answer")
    team = relationship("Team", back_populates="teamanswer")
    gamer = relationship("Gamer", back_populates="teamanswer")
    tourquestion = relationship("TourQuestion", back_populates="teamanswer")

    def __init__(self, id=None, answer=None, is_correct=None, is_recognized=None, team_id=None, gamer_id=None,
                 game_id=None, question_id=None, answer_dttm=None, question=None, team=None, gamer=None,
                 tourquestion=None):
        self.id = id
        self.answer = answer
        self.is_correct = is_correct
        self.is_recognized = is_recognized
        self.team_id = team_id
        self.gamer_id = gamer_id
        self.game_id = game_id
        # self.question_id = question_id
        self.answer_dttm = answer_dttm
        # self.question = question
        # self.team = team
        # self.gamer = gamer
        # self.tourquestion = tourquestion


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
    teamanswer = relationship("TeamAnswer", back_populates="gamer")
    team = relationship("Team", back_populates="gamer", secondary='team_x_gamer')
    #gamer_x_game = relationship("Game", back_populates="gamer", secondary='Game_x_Gamer_Team')

    def __init__(self, id=None, first_name=None, last_name=None, nick_name=None, chat_id=None, gamer_phone=None,
                 gamer_email=None, teamanswer=None, team=None, gamer_x_game=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.nick_name = nick_name
        self.chat_id = chat_id
        self.gamer_phone = gamer_phone
        self.gamer_email = gamer_email
        # self.teamanswer = teamanswer
        # self.team = team
        # self.gamer_x_game = gamer_x_game


class Team(Base):
    __tablename__ = 'team'
    id = Column(Integer, primary_key=True)
    team_name = Column(String(120))
    team_slogan = Column(String(120))
    team_phone = Column(String(120))
    team_email = Column(String(120))
    team_current_cap = Column(Integer, ForeignKey('gamer.id'))

    # game_link = relationship("Game2Team")
    gamer = relationship("Gamer", back_populates="team", secondary='team_x_gamer')
    game = relationship("Game", back_populates="team", secondary='team_x_game')
    gamer_x_game = relationship("Gamer", back_populates="team", secondary='game_x_gamer_team')
    teamanswer = relationship("TeamAnswer", back_populates="team")

    def __init__(self, id=None, team_name=None, team_slogan=None, team_phone=None, team_email=None,
                 team_current_cap=None, game_link=None, gamer=None, gamer_x_game=None):
        self.id = id
        self.team_name = team_name
        self.team_slogan = team_slogan
        self.team_phone = team_phone
        self.team_email = team_email
        self.team_current_cap = team_current_cap
        # self.game_link = game_link
        # self.gamer = gamer
        # self.gamer_x_game = gamer_x_game


class Team_x_Gamer(Base):
    __tablename__ = 'team_x_gamer'
    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('team.id'))
    gamer_id = Column(Integer, ForeignKey('gamer.id'))

    def __init__(self, id=None, team_id=None, gamer_id=None):
        self.id = id
        self.team_id = team_id
        self.gamer_id = gamer_id


class Team_x_Game(Base):
    __tablename__ = 'team_x_game'
    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('team.id'))
    game_id = Column(Integer, ForeignKey('game.id'))

    def __init__(self, id=None, team_id=None, game_id=None):
        self.id = id
        self.team_id = team_id
        self.game_id = game_id


class Game_x_Gamer_Team(Base):
    __tablename__ = 'game_x_gamer_team'
    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('game.id'))
    team_id = Column(Integer, ForeignKey('team.id'))
    gamer_id = Column(Integer, ForeignKey('gamer.id'))
    is_captain = Column(Integer)

    def __init__(self, id=None, game_id=None, team_id=None, gamer_id=None, is_captain=None):
        self.id = id
        self.game_id = game_id
        self.team_id = team_id
        self.gamer_id = gamer_id
        self.is_captain = is_captain


class Masters(Base):
    __tablename__ = 'master'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(120))
    last_name = Column(String(120))
    nick_name = Column(String(120))
    master_role = Column(String(120))

    def __init__(self, id=None, first_name=None, last_name=None, nick_name=None, master_role=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.nick_name = nick_name
        self.master_role = master_role


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
