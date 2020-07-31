# ------------------------------------------------------------------------
# database.py: db layer program for Audio Tagging application
# ------------------------------------------------------------------------


''' using my IW as a template for setting up functions with SQLAlchemy, 
but we can change this if people like something else better! '''

from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import FLOAT

# --------------------------------------------------------------------------
# helpful resource:
# https://www.compose.com/articles/using-postgresql-through-sqlalchemy/
# --------------------------------------------------------------------------


# PostgreSQL URL (db is saved locally on my comp so not sure if others can connect)
# db_string = "postgresql://carinalewandowski:nautilusinternship2020@127.0.0.1/audio_test_db"
db_string = "postgres://iromfnjf:VasJUQYZnTDLk3I5Rfk7zWsXc5WdZKjB@ruby.db.elephantsql.com:5432/iromfnjf"
# to set up with tableplus:
# name: audio-tagging-test
# host/socket: ruby.db.elephantsql.com
# port: 5432
# user: iromfnjf
# password: VasJUQYZnTDLk3I5Rfk7zWsXc5WdZKjB
# database: iromfnjf
Base = declarative_base()


# table for storing audio file title along with descriptive parameters
class Audio_Params(Base):
    __tablename__ = 'audio_params'
    # __tablename__ = 'iromfnjf'
    uri = Column(String, primary_key=True)
    jazz = Column(FLOAT())
    rb = Column(FLOAT())
    rock = Column(FLOAT())
    country = Column(FLOAT())
    dance = Column(FLOAT())
    hh = Column(FLOAT())
    classical = Column(FLOAT())
    pop = Column(FLOAT())
    ed = Column(FLOAT())
    speed = Column(FLOAT())
    vol = Column(FLOAT())
    valence = Column(FLOAT())
    instru = Column(FLOAT())
    tag_count = Column(Integer, default=0)

    # get all results from table
    def get_all(self):
        results = session.query(Audio_Params)
        return results

    # get row in table with the given audio file title
    def get_row(self, title):
        results = session.query(Audio_Params)
        row = results.filter(Audio_Params.uri == uri)
        return row

    # add a new row to the table with the given audio file title and 
    # descriptive parameters
    def add_row(self, title, params):
        row = Audio_Params(uri=title,
                           jazz=params[0],
                           rb=params[1],
                           rock=params[2],
                           country=params[3],
                           dance=params[4],
                           hh=params[5],
                           classical=params[6],
                           pop=params[7],
                           ed=params[8],
                           speed=params[9],
                           vol=params[10],
                           valence=params[11],
                           instru=params[12])
        session.add(row)
        session.commit()

    # Update the database if the song title exists already in the database
    # what does sessions.query return?
    # what does get_row return?
    # how do you update a row in the database
    def update_row(self, title, params):
        # returns a row object from the database
        row = self.get_row(title)
        # make this row object a dictionary
        row_dict = row.__dict__
        print(row_dict)
        if len(row_dict) == 0:
            self.add_row(self, title, params)
        else:
            i = 0
            for key in row_dict:
                if key != "title":  # not sure if this is what the key is called
                    # need to get user_confidence
                    row_dict[key] = (row_dict[key] + params[i] * user_confidence) / (2 - (1 - user_confidence))
                    # is this how you update?
                    session.query(row).update({key: row_dict[key]})
                    i += 1

    # delete row in table with the given audio file title
    # NOTE: for now, using file title to id files, but if we had a large dataset
    # where multiple songs have the same title, we'd want to add an id param
    def del_row(self, title):
        # assume only one result with title, so pick entry at index 0
        row = self.get_row(title)[0]
        session.delete(row)
        session.commit()


# connect to database
db = create_engine(db_string)
Session = sessionmaker(db)
session = Session()

# test add row
# title = "test new db!"
# params = [0.1, 0.22, 0, 0.1, 0.1, 0.6, 0.1, 0, 0.1, 0.1, 0.1, 1, 1]
# audioP = Audio_Params()
# audioP.add_row(title, params)
# # test get row
# # assume only one result with title, so pick entry at index 0
# row = audioP.get_row(title)[0]
# print(str(row.title))
# # test delete row
# # audioP.del_row(title)

# # disconnect
# session.close()
