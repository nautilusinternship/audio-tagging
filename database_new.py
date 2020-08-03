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
JAZZ = 0
RB = 1
ROCK = 2
COUNTRY = 3
DANCE = 4
HH = 5
CLASSICAL = 6
POP = 7
ED = 8
SPEED = 9
VOL = 10
VALENCE = 11
INSTRU = 12

# table for storing audio file title along with descriptive parameters
class Audio_Params(Base):
    __tablename__ = 'audio_params_new'
    # __tablename__ = 'iromfnjf'
    uri = Column(String, primary_key=True)
    jazz = Column(JSON)
    rb = Column(JSON)
    rock = Column(JSON)
    country = Column(JSON)
    dance = Column(JSON)
    hh = Column(JSON)
    classical = Column(JSON)
    pop = Column(JSON)
    ed = Column(JSON)
    speed = Column(JSON)
    vol = Column(JSON)
    valence = Column(JSON)
    instru = Column(JSON)
    tag_count = Column(Integer, default=1)

    # get all results from table
    def get_all(self):
        results = session.query(Audio_Params)
        return results

    # get row in table with the given audio file title
    def get_row(self, uri):
        results = session.query(Audio_Params)
        # get the first row with matching URI (should only be 1 row anyway)
        row = results.filter(Audio_Params.uri == uri)[0]
        return row

    def check_exists(self, uri):
        results = session.query(Audio_Params)
        for result in results:
            if result.uri == uri:
                return True
        return False


    # add a new row to the table with the given audio file title and
    # descriptive parameters
    def add_row(self, uri, dict_list, tag_count):
        row = Audio_Params(uri=uri,
                           jazz=dict_list[JAZZ],
                           rb=dict_list[RB],
                           rock=dict_list[ROCK],
                           country=dict_list[COUNTRY],
                           dance=dict_list[DANCE],
                           hh=dict_list[HH],
                           classical=dict_list[CLASSICAL],
                           pop=dict_list[POP],
                           ed=dict_list[ED],
                           speed=dict_list[SPEED],
                           vol=dict_list[VOL],
                           valence=dict_list[VALENCE],
                           instru=dict_list[INSTRU],
                           tag_count=tag_count)
        session.add(row)
        session.commit()

    # Update the database if the song title exists already in the database
    # how do you update a row in the database
    def update_row(self, uri, user_dict_list):
        # get existing row
        if self.check_exists(uri):
            row = self.get_row(uri)
    
            tag_count = row.tag_count
            # create db dict list
            db_dict_list = [row.jazz, row.rb, row.rock, row.country, row.dance, row.hh,
            row.classical, row.pop, row.ed, row.speed, row.vol, row.valence, row.instru]

            new_db_dict_list = []
            i = 0
            while i < len(db_dict_list):
                # get current num, and denom for a param from db
                num = db_dict_list[i]['num']
                denom = db_dict_list[i]['denom']
                # get user rating and conf from input
                user_rating = user_dict_list[i]['rating']
                user_conf = user_dict_list[i]['conf']
                # calculate new rating, num, and denom for db
                new_db_dict_list.append(self.calc_db_dict_list(num, denom, user_rating, user_conf))

                i+=1
            

            # delete existing row
            session.delete(row)
            session.commit()
            # add new updated row
            self.add_row(uri, new_db_dict_list, tag_count + 1) 
            session.commit()

        else:
            new_db_dict_list = []
            i = 0
            while i < len(user_dict_list):
                # get user rating and conf from input
                user_rating = user_dict_list[i]['rating']
                user_conf = user_dict_list[i]['conf']
                # calculate new rating, num, and denom for db
                new_db_dict_list.append(self.calc_db_dict_list(float(0), float(0), user_rating, user_conf))

                i+=1

            self.add_row(uri, new_db_dict_list, 1) 
            session.commit()
        
    def calc_db_dict_list(self, num, denom, user_rating, user_conf):
        # calculate new weighted average
        new_num = num + (user_rating*user_conf)
        new_denom = denom + user_conf
        new_rating = new_num/new_denom
        db_dict_item = {}
        db_dict_item['rating'] = new_rating
        db_dict_item['num'] = new_num
        db_dict_item['denom'] = new_denom
        return db_dict_item

    # grab a row with the given uri but only have the genre columns
    def get_genres(self, uri):
        genres = session.query(Audio_Params).filter(Audio_Params.uri == uri). \
            options(load_only("jazz", "rb", "rock", "country", "dance", "hh", "classical", "pop", "ed",
                              "speed", "vol", "valence", "instru"))
        return genres

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
# test get row
# assume only one result with title, so pick entry at index 0
# row = audioP.get_row("0hCB0YR03f6AmQaHbwWDe8")
# print(str(row.jazz))
# # test delete row
# # audioP.del_row(title)

# disconnect
# session.close()

# NEW TESTS

'''audioP = Audio_Params()
uri = "testing new functions"
dict_list = []

i = 0
while i < 13:
    dict_item = {
        'rating': 0.9,
        'conf': 0.8
    }
    dict_list.append(dict_item)
    i+=1
print(dict_list)
audioP.update_row(uri, dict_list) '''
