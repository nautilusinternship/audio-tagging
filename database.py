# ------------------------------------------------------------------------
# database.py: db layer program for Audio Tagging application
# ------------------------------------------------------------------------


''' using my IW as a template for setting up functions with SQLAlchemy, 
but we can change this if people like something else better! '''

from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import FLOAT

# --------------------------------------------------------------------------
# helpful resource:
# https://www.compose.com/articles/using-postgresql-through-sqlalchemy/
# --------------------------------------------------------------------------


# PostgreSQL URL (db is saved locally on my comp so not sure if others can connect)
db_string = "postgresql://carinalewandowski:nautilusinternship2020@127.0.0.1/audio_test_db"

Base = declarative_base()

# table for storing audio file title along with descriptive parameters
class Audio_Params(Base):
    __tablename__ = 'audio_params'
    title = Column(String, primary_key=True)
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

    # get all results from table
    def get_all(self):
        results = session.query(Audio_Params)
        return results

    # get row in table with the given audio file title
    def get_row(self, title):
        results = session.query(Audio_Params)
        row = results.filter(Audio_Params.title == title)
        return row

    # add a new row to the table with the given audio file title and 
    # descriptive parameters
    def add_row(self, title, params):
        row = Audio_Params(title=title,
            jazz = params[0],
            rb = params[1],
            rock = params[2],
            country = params[3],
            dance = params[4],
            hh = params[5],
            classical = params[6],
            pop = params[7],
            ed = params[8],
            speed = params[9],
            vol = params[10],
            valence = params[11],
            instru = params[12])
        session.add(row)
        session.commit()
    
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
title = "fake song part 3"
params = [0.1, 0.22, 0, 0.1, 0.1, 0.6, 0.1, 0, 0.1, 0.1, 0.1, 1, 1]
audioP = Audio_Params()
# audioP.add_row(title, params)
# test get row
# assume only one result with title, so pick entry at index 0
row = audioP.get_row(title)[0]
print(str(row.title))
# test delete row
# audioP.del_row(title)

# disconnect
session.close()