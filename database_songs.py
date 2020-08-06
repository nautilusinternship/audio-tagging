# ------------------------------------------------------------------------
# database.py: db layer program for Audio Tagging application
# ------------------------------------------------------------------------


''' using my IW as a template for setting up functions with SQLAlchemy, 
but we can change this if people like something else better! '''

from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import FLOAT, JSON
from sqlalchemy.orm import load_only
import random
import math

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

# CONSTANTS
# URI = 0
TITLE = 0
ARTIST = 1

# table for storing audio file title along with descriptive parameters
class Song(Base):
    __tablename__ = 'songs'
    # __tablename__ = 'iromfnjf'
    uri = Column(String, primary_key=True)
    title = Column(String)
    artist = Column(String)
    tag_count = Column(Integer, default=0)


    # get all results from table
    def get_song(self):
        # gets random song in upper half of database sorted by tag count
        rand = random.randrange(0, math.floor(session.query(Song).count() / 2)) 
        results = list(session.query(Song).order_by(Song.tag_count))
        return results[rand]

    # get all results from table
    def get_all(self):
        results = session.query(Song)
        return results

    # get row in table with the given audio file title
    def get_row(self, uri):
        results = session.query(Song)
        # get the first row with matching URI (should only be 1 row anyway)
        row = results.filter(Song.uri == uri)[0]
        return row

    def check_exists(self, uri):
        results = session.query(Song)
        for result in results:
            if result.uri == uri:
                return True
        return False


    # add a new row to the table with the given audio file title and
    # descriptive parameters
    def add_row(self, uri, params, tag_count):
        row = Song(uri=uri,
                    title=params[TITLE],
                    artist=params[ARTIST],
                    tag_count=tag_count)
        session.add(row)
        session.commit()

    # Update the database if the song title exists already in the database
    # how do you update a row in the database
    def update_row(self, uri, params):
        # get existing row
        if self.check_exists(uri):
            # update tag count
            row = self.get_row(uri)
            tag_count = row.tag_count
            
            # delete existing row
            session.delete(row)
            session.commit()

            # params = []
            # params.append(row.title, row.artist)
            # add new updated row
            self.add_row(uri, params, tag_count + 1) 
            session.commit()

        else:
            # no song detected - put 0
            self.add_row(uri, params, 0)
            session.commit()
        

    # grab a row with the given uri but only have the genre columns
    def get_genres(self, uri):
        genres = session.query(Song).filter(Song.uri == uri). \
            options(load_only("jazz", "rb", "rock", "country", "dance", "hh", "classical", "pop", "ed",
                              "speed", "vol", "valence", "instru"))
        return genres

    # delete row in table with the given audio file title
    # NOTE: for now, using file title to id files, but if we had a large dataset
    # where multiple songs have the same title, we'd want to add an id param

    def del_row(self, uri):
        # assume only one result with title, so pick entry at index 0
        row = self.get_row(uri)[0]
        session.delete(row)
        session.commit()


# connect to database
db = create_engine(db_string)
Session = sessionmaker(db)
session = Session()

# test add row
# title = "test new db!"
# params = [0.1, 0.22, 0, 0.1, 0.1, 0.6, 0.1, 0, 0.1, 0.1, 0.1, 1, 1]
# audioP = Song()
# audioP.add_row(title, params)
# test get row
# assume only one result with title, so pick entry at index 0
# row = audioP.get_row("0hCB0YR03f6AmQaHbwWDe8")
# print(str(row.jazz))
# # test delete row
# # audioP.del_row(title)

# disconnect
# session.close()

# NEW TESTS
# song = Song()
# uri="spotify:track:5f5j72fj7bZkfqSdeSWLyf"
# params = ['Why Does It Take So Long To Say Goodbye', 'Joe Bonamassa']
# song.update_row(uri, params)

# r = song.get_song()
# print(r.title)
# print(r.artist)

# for s in songs:
#     print(s.tag_count)
# print(song.get_row(uri))

# ADDING CURRENT SONGS
'''
songDB = Song()
import csv
with open('test1doc.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        # TITLE = lines[0], 
        # ARTIST = lines[1], 
        # URI = lines[2]
        lines = list(readCSV)
        for line in lines:
            songDB.update_row(line[2], line[:2]) 
'''
