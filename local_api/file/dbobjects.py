from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


#from threading import Thread

DatabaseBase = declarative_base()

class DatabaseHandler:
	def __init__(self):
		pass

	def startDB(self):
		self.engine = create_engine('sqlite:///local_storage/master.db', connect_args={'check_same_thread':False})
		DatabaseBase.metadata.create_all(self.engine)
		self.sessionMaker = sessionmaker()
		self.sessionMaker.configure(bind=self.engine)

	def createNewSession(self):
		session = self.sessionMaker()
		return session

	def addObject(self, obj, session=None):
		needSave = False
		if session == None:
			session = self.createNewSession()
			needSave = True
		session.add(obj)
		if needSave:
			self.saveSession(session)

	def saveSession(self, session):
		session.commit()

GlobalDatabaseHandler = DatabaseHandler()
# To use the databse, import the GlobalDatabaseHandler and then proceed as normal with
# sqlalchemy database usage.
