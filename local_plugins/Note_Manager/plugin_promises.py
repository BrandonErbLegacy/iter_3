from local_api.network.twisted_promises import Promises, Promise
from local_promises.required_promises import AuthenticatePromise
from local_objects.required_objects import Session
from local_api.file.dbobjects import GlobalDatabaseHandler
from getpass import getpass
from uuid import uuid4

from local_plugins.Note_Manager.plugin_objects import Notebook, NoteCategory, NoteCategory_Note_Relation, NotebookPage

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
				dbSession.close()
			else:
				return

		local_node.fetchDataFromBuffer("NOTE_MANAGER_GET_SESSION_ID", getNoteList)


class Note_Manager_List_Notes_By_Multiple_Category_ID(Promise):
	#Lists notes with all categories
	pass

class Note_Manager_Create_Notebook(Promise):
	@AuthenticatePromise
	def clientAction(self, **kw):
		sessionID = self._register.getEnvironmentVariable("AUTHENTICATION_SESSION_ID")
		self._register.sendData("NOTE_MANAGER_GET_SESSION_ID", sessionID)

		self._register.fetchDataFromBuffer("NEW_NOTEBOOK_AND_PAGE", lambda data: kw["func"](data))

	@AuthenticatePromise
	def serverAction(self, **kw):
		local_node = kw["NODE"]
		dbSession = GlobalDatabaseHandler.createNewSession()

		def receivedUserSession(sessionID):
			userID = getUserBySession(sessionID, dbSession, getPeerIP(local_node))
			if userID != None:
				newNotebookID = str(uuid4())
				newNotebook = Notebook()
				newNotebook.id = newNotebookID
				newNotebook.createdByID = userID
				newNotebook.permissionID = str(uuid4())
				newNotebook.title = "New Notebook"

				newNotebookPageDefault = NotebookPage()
				newNotebookPageDefault.id = str(uuid4())
				newNotebookPageDefault.permissionID = str(uuid4())
				newNotebookPageDefault.createdByID = userID
				newNotebookPageDefault.content = "New Page"
				newNotebookPageDefault.notebook_id = newNotebookID
				newNotebookPageDefault.title = "N"

				local_node.sendData("NEW_NOTEBOOK_AND_PAGE", (newNotebook, newNotebookPageDefault))

				GlobalDatabaseHandler.addObject(newNotebook, dbSession)
				GlobalDatabaseHandler.addObject(newNotebookPageDefault, dbSession)
				GlobalDatabaseHandler.saveSession(dbSession)

				dbSession.close()
			else:
				return
		local_node.fetchDataFromBuffer("NOTE_MANAGER_GET_SESSION_ID", receivedUserSession)

class Note_Manager_Get_Notebook_Pages(Promise):
	@AuthenticatePromise
	def clientAction(self, **kw):
		sessionID = self._register.getEnvironmentVariable("AUTHENTICATION_SESSION_ID")
		self._register.sendData("NOTE_MANAGER_GET_SESSION_ID", sessionID)
		self._register.sendData("NOTEBOOK_ID", kw["notebookID"])

		self._register.fetchDataFromBuffer("NOTEBOOK_PAGES", lambda data: kw["func"](data))

	@AuthenticatePromise
	def serverAction(self, **kw):
		local_node = kw["NODE"]
		dbSession = GlobalDatabaseHandler.createNewSession()

		def receivedNotebookID(userID, NotebookID):
			notebookPages = dbSession.query(NotebookPage).filter(NotebookPage.notebook_id == NotebookID).\
			filter(NotebookPage.createdByID == userID).all()
			local_node.sendData("NOTEBOOK_PAGES", notebookPages)
			dbSession.close()

		def receivedUserSession(sessionID):
			userID = getUserBySession(sessionID, dbSession, getPeerIP(local_node))
			if userID != None:
				local_node.fetchDataFromBuffer("NOTEBOOK_ID", lambda data: receivedNotebookID(userID, data))
			else:
				return
		local_node.fetchDataFromBuffer("NOTE_MANAGER_GET_SESSION_ID", receivedUserSession)

class Note_Manager_Create_Notebook_Page(Promise):
	@AuthenticatePromise
	def clientAction(self, **kw):
		sessionID = self._register.getEnvironmentVariable("AUTHENTICATION_SESSION_ID")
		#notebookID = 
		#notebookName = self._register.get
		self._register.sendData("NOTE_MANAGER_GET_SESSION_ID", sessionID)
		self._register.sendData("NOTE_MANAGER_NOTEBOOK_PAGE_DETAILS", ())

		#self._register.fetchDataFromBuffer("NEW_NOTEBOOK_PAGE", lambda data: kw["func"](data))

	@AuthenticatePromise
	def serverAction(self, **kw):
		local_node = kw["NODE"]
		dbSession = GlobalDatabaseHandler.createNewSession()

		def receivedUserSession(sessionID):
			userID = getUserBySession(sessionID, dbSession, getPeerIP(local_node))
			if userID != None:
				#Create NotebookPage

				dbSession.close()
			else:
				return
		local_node.fetchDataFromBuffer("NOTE_MANAGER_GET_SESSION_ID", receivedUserSession)

class Note_Manager_Update_Notebook(Promise):
	pass

class Note_Manager_Delete_Notebook(Promise):
	pass

class Note_Manager_Update_Notebook_Page(Promise):
	pass

class Note_Manager_Delete_Notebook_Page(Promise):
	pass

class Note_Manager_Update_Category_Relation(Promise):
	#Also adds category relations
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
Promises.register(Note_Manager_Create_Notebook())
Promises.register(Note_Manager_Get_Notebook_Pages())
