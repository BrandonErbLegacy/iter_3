from local_api.file.dbobjects import DatabaseBase

from sqlalchemy import Column, Integer, String, DateTime

class User(DatabaseBase):
	__tablename__ = "Users"

	id = Column(String(36), primary_key=True)
	username = Column(String)
	password = Column(String)
	salt = Column(String(36))

class Session(DatabaseBase):
	__tablename__ = "Sessions"

	id = Column(String(36), primary_key=True)
	userID = Column(String(36))
	addressIssued = Column(String)
