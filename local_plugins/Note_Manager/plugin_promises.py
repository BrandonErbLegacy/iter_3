from local_api.network.twisted_promises import Promises, Promise
from local_promises.required_promises import AuthenticatePromise
from local_objects.required_objects import Session
from local_api.file.dbobjects import GlobalDatabaseHandler
from getpass import getpass
from uuid import uuid4

from local_plugins.Note_Manager.plugin_objects import Notebook, NoteCategory, NoteCategory_Note_Relation

from local_api.helpers.accessControl import getUserBySession, getPeerIP

class Note_Manager_List_Notes(Promise):
	@AuthenticatePromise
	def clientAction(self, **kw):
		sessionID = self._register.getEnvironmentVariable("AUTHENTICATION_SESSION_ID")

		self._register.sendData("NOTE_MANAGER_GET_SESSION_ID", sessionID)

		self._register.fetchDataFromBuffer("NOTE_MANAGER_LIST", lambda data: kw["func"](data))

	@AuthenticatePromise
	def serverAction(self, **kw):
		local_node = kw["NODE"]

		dbSession = GlobalDatabaseHandler.createNewSession()

		def getNoteList(sessionID):
			userID = getUserBySession(sessionID, dbSession, getPeerIP(local_node))
			if userID != None:
				notebooks = dbSession.query(Notebook).filter(Notebook.createdByID == userID).all()
				local_node.sendData("NOTE_MANAGER_LIST", notebooks)
			else:
				return

		local_node.fetchDataFromBuffer("NOTE_MANAGER_GET_SESSION_ID", getNoteList)


class Note_Manager_List_Notes_By_Multiple_Category_ID(Promise):
	#Lists notes with all categories
	pass

class Note_Manager_Create_Note(Promise):
	def clientAction(self, **kw):
		pass

	def serverAction(self, **kw):
		pass

class Note_Manager_Update_Note(Promise):
	pass

class Note_Manager_Delete_Note(Promise):
	pass

class Note_Manager_Update_Category_Relation(Promise):
	pass

class Note_Manager_List_Categories(Promise):
	pass

class Note_Manager_Create_Category(Promise):
	pass

class Note_Manager_Update_Category(Promise):
	pass

class Note_Manager_Delete_Category(Promise):
	pass

Promises.register(Note_Manager_List_Notes())
Promises.register(Note_Manager_Create_Note())
