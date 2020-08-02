# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy import Column, Integer, String
# from sqlalchemy.dialects.postgresql import FLOAT
# from sqlalchemy.orm import load_only
#
# engine = create_engine(, echo=True)
# Base = declarative_base()
# Session = sessionmaker(bind=engine)
# session = Session()
#
#
# class Audio_Param(Base):
#     __tablename__ = 'audio_param'
#     uri = Column(String, primary_key=True)
#     jazz = Column(FLOAT())
#     jazz_conf = Column(FLOAT())
#     rb = Column(FLOAT())
#     rb_conf = Column(FLOAT())
#
#     # get all results from table
#     def get_all(self):
#         results = session.query(Audio_Param)
#         return results
#
#     # get row in table with the given audio file title
#     def get_row(self, uri):
#         results = session.query(Audio_Param)
#         row = results.filter(Audio_Param.uri == uri)
#         return row
#
#     # add a new row to the table with the given audio file title and
#     # descriptive parameters
#     def add_row(self, uri, params):
#         row = Audio_Param(uri=uri,
#                           jazz=params[0],
#                           jazz_conf=params[1],
#                           rb=params[2],
#                           rb_conf=params[3],)
#         session.add(row)
#         session.commit()
#
#     # Update the database if the song title exists already in the database
#     # what does sessions.query return?
#     # what does get_row return?
#     # how do you update a row in the database
#     def update_row(self, uri, params):
#         # returns a row object from the database
#         row = self.get_row(uri)
#         # make this row object a dictionary
#         row_dict = row.__dict__
#         print(row_dict)
#         if len(row_dict) == 0:
#             self.add_row(uri, params)
#         else:
#             i = 0
#             for key in row_dict:
#                 if key != "uri":  # not sure if this is what the key is called
#                     # need to get user_confidence
#                     row_dict[key] = (row_dict[key] + params[i]
#                                      * params[i + 1]) / (2 - (1 - user_confidence))
#                     # is this how you update?
#                     session.query(row).update({key: row_dict[key]})
#                     i += 2
#
#     def get_genres(self):
#         genres = session.query(Audio_Param).options(load_only("jazz", "rb"))
#         print(genres)
#
#
# # audio1 = Audio_Param(uri="try1", jazz="0.3", jazz_conf="0.5", rb="0.7", rb_conf="0.3")
# # audio2 = Audio_Param(uri="try2", jazz="0.6", jazz_conf="0.2", rb="0.9", rb_conf="0.1")
# # session.add_all([audio1, audio2])
# # session.commit()
# users = session.query(Audio_Param).filter(Audio_Param.uri == "5MxNLUsfh7uzROypsoO5qe").options(load_only("jazz", "rb"))
# # users = session.query(Audio_Param).all()
# print(users)
# # for user in users:
# #     print(user.__dict__)