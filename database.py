# ------------------------------------------------------------------------
# database.py: db layer program for Audio Tagging application
# ------------------------------------------------------------------------


''' using my IW as a template for setting up functions with SQLAlchemy, 
but we can change this if people like something else better! '''

from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import FLOAT
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


# table for storing audio file title along with descriptive parameters
class Audio_Params(Base):
    __tablename__ = 'audio_params'
    # __tablename__ = 'iromfnjf'
    uri = Column(String, primary_key=True)
    jazz = Column(FLOAT())
    jazz_conf = Column(FLOAT())
    rb = Column(FLOAT())
    rb_conf = Column(FLOAT())
    rock = Column(FLOAT())
    rock_conf = Column(FLOAT())
    country = Column(FLOAT())
    country_conf = Column(FLOAT())
    dance = Column(FLOAT())
    dance_conf = Column(FLOAT())
    hh = Column(FLOAT())
    hh_conf = Column(FLOAT())
    classical = Column(FLOAT())
    classical_conf = Column(FLOAT())
    pop = Column(FLOAT())
    pop_conf = Column(FLOAT())
    ed = Column(FLOAT())
    ed_conf = Column(FLOAT())
    speed = Column(FLOAT())
    speed_conf = Column(FLOAT())
    vol = Column(FLOAT())
    vol_conf = Column(FLOAT())
    valence = Column(FLOAT())
    valence_conf = Column(FLOAT())
    instru = Column(FLOAT())
    instru_conf = Column(FLOAT())
    tag_count = Column(Integer, default=1)

    # get all results from table
    def get_all(self):
        results = session.query(Audio_Params)
        return results

    # get row in table with the given audio file title
    def get_row(self, uri):
        results = session.query(Audio_Params)
        row = results.filter(Audio_Params.uri == uri)
        return row

    # add a new row to the table with the given audio file title and
    # descriptive parameters
    def add_row(self, uri, result_dict):
        row = Audio_Params(uri=uri,
                           jazz=result_dict["jazz"],
                           jazz_conf=result_dict["jazz-conf"],
                           rb=result_dict["rb"],
                           rb_conf=result_dict["rb-conf"],
                           rock=result_dict["rock"],
                           rock_conf=result_dict["rock-conf"],
                           country=result_dict["country"],
                           country_conf=result_dict["country-conf"],
                           dance=result_dict["dance"],
                           dance_conf=result_dict["dance-conf"],
                           hh=result_dict["hh"],
                           hh_conf=result_dict["hh-conf"],
                           classical=result_dict["classical"],
                           classical_conf=result_dict["classical-conf"],
                           pop=result_dict["pop"],
                           pop_conf=result_dict["pop-conf"],
                           ed=result_dict["ed"],
                           ed_conf=result_dict["ed-conf"],
                           speed=result_dict["speed"],
                           speed_conf=result_dict["speed-conf"],
                           vol=result_dict["vol"],
                           vol_conf=result_dict["vol-conf"],
                           valence=result_dict["valence"],
                           valence_conf=result_dict["valence-conf"],
                           instru=result_dict["instru"],
                           instru_conf=result_dict["instru-conf"])
        session.add(row)
        session.commit()

    # Update the database if the song title exists already in the database
    # how do you update a row in the database
    def update_row(self, uri, results_dict):
        # returns a row object from the database
        row = self.get_row(uri)
        # make it dict
        row_dict = row.first().__dict__
        if not session.query(row.exists()).scalar():
            self.add_row(uri, results_dict)
        else:
            db_object = self.get_genres(uri)
            for obj in db_object:
                genres = obj.__dict__
                for genre in genres:
                    if genre != "uri" and genre != "_sa_instance_state":
                        row_conf = genre + "_conf"
                        results_conf = genre + "-conf"
                        # update genre ratings
                        # Need more robust formula
                        row_dict[genre] = self.vector_equation(results_dict[results_conf], row_dict[row_conf],
                                                               row_dict[genre], results_dict[genre])
                        # update confidence levels associated with each genre rating
                        row_dict[row_conf] = (row_dict[row_conf] + results_dict[results_conf]) / row_dict["tag_count"]
                        # THIS NEEDS WORK: currently does not update the rows
                        row.update({genre: row_dict[genre]})
                        row.update({row_conf: row_dict[row_conf]})
                        row.update({"tag_count": row_dict["tag_count"] + 1})

    # need to make sure current_conf is never zero
    def vector_equation(self, user_conf, current_conf, current_rating, user_rating):
        if current_conf == 0:
            raise ValueError("Current confidence should never be 0")
        if current_conf < user_conf:
            return (current_rating + user_rating * user_conf) / (2 - (1 - current_conf / user_conf))
        else:
            return (current_rating + user_rating * user_conf) / (2 - (1 - user_conf / current_conf))

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
# # test get row
# # assume only one result with title, so pick entry at index 0
# row = audioP.get_row(title)[0]
# print(str(row.title))
# # test delete row
# # audioP.del_row(title)

# # disconnect
# session.close()
