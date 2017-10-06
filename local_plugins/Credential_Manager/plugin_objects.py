from local_api.file.dbobjects import DatabaseBase

from sqlalchemy import Column, Integer, String, DateTime

class Credential(DatabaseBase):
	__tablename__ = "credentials"

	id = Column(String(36), primary_key=True)
	username = Column(String)
	password = Column(String)
	target = Column(String)
	notes = Column(String)
	displayName = Column(String)
