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
		"""Takes 1 argument
		func: The function to be executed once the notebooks have been listed
		Returns a list of notebooks on the server
		"""
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
		"""Takes 1 argument
		func: The function to execute once a new page and notebook have been created
		Returns the new page and notebook
		"""
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
		"""Takes 2 arguments.
		notebookID: The ID of the notebook you're fetching pages from (UUID4)
		func: The function to execute with the return data
		Returns a list of notebook pages for the specified ID, or None
		"""
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
		"""Takes 3 key args.
		 notebookID: UUID4 of the desired notebook
		 notebookTitle: String for the title
		 func: The function to be executed with the completion status of the promise
		 Returns: None if unsuccessful, or NotebookPage if successful"""
		sessionID = self._register.getEnvironmentVariable("AUTHENTICATION_SESSION_ID")
		notebookID, notebookTitle = kw["notebookID"], kw["notebookTitle"]
		self._register.sendData("NOTE_MANAGER_GET_SESSION_ID", sessionID)
		self._register.sendData("NOTE_MANAGER_NOTEBOOK_PAGE_DETAILS", (notebookID, notebookTitle))

		self._register.fetchDataFromBuffer("NOTE_MANAGER_NEW_NOTEBOOK_PAGE_RESULT", lambda data: kw["func"](data))

	@AuthenticatePromise
	def serverAction(self, **kw):
		local_node = kw["NODE"]
		dbSession = GlobalDatabaseHandler.createNewSession()

		def createNotebookPage(notebookPage_title_tuple, userID):
			notebookID, notebookTitle = notebookPage_title_tuple
			#TODO: Validate user has permission to create this new notebook page on the notebook
			newNotebookPageDefault = NotebookPage()
			newNotebookPageDefault.id = str(uuid4())
			newNotebookPageDefault.permissionID = str(uuid4())
			newNotebookPageDefault.createdByID = userID
			newNotebookPageDefault.content = ""
			newNotebookPageDefault.notebook_id = notebookID
			newNotebookPageDefault.title = notebookTitle

			local_node.sendData("NOTE_MANAGER_NEW_NOTEBOOK_PAGE_RESULT", newNotebookPageDefault)

			GlobalDatabaseHandler.addObject(newNotebookPageDefault, dbSession)
			GlobalDatabaseHandler.saveSession(dbSession)

			dbSession.close()

		def receivedUserSession(sessionID):
			userID = getUserBySession(sessionID, dbSession, getPeerIP(local_node))
			if userID != None:
				#Create NotebookPage
				local_node.fetchDataFromBuffer("NOTE_MANAGER_NOTEBOOK_PAGE_DETAILS", lambda data: createNotebookPage(data, userID))
			else:
				return
		local_node.fetchDataFromBuffer("NOTE_MANAGER_GET_SESSION_ID", receivedUserSession)

class Note_Manager_Update_Notebook(Promise):
	def clientAction(self, **kw):
		"""Takes 2 arguments:
		notebookObj: This is the Notebook to be updated
		func: The function to be executed once the notebook has been updated
		Returns an updated Notebook object or None"""
		sessionID = self._register.getEnvironmentVariable("AUTHENTICATION_SESSION_ID")
		notebook = kw["notebookObj"]
		self._register.sendData("NOTE_MANAGER_GET_SESSION_ID", sessionID)
		self._register.sendData("NOTE_MANAGER_NOTEBOOK_DETAILS", notebook)
		print("Sending Notebook")

		self._register.fetchDataFromBuffer("NOTE_MANAGER_UPDATE_NOTEBOOK_RESULT", lambda data: kw["func"](data))

	def serverAction(self, **kw):
		local_node = kw["NODE"]
		dbSession = GlobalDatabaseHandler.createNewSession()

		def createNotebookPage(notebookObj, userID):
			notebook = notebookObj
			liveObject = dbSession.query(Notebook).filter(Notebook.createdByID == userID).filter(Notebook.id == notebook.id).one()
			liveObject.title = notebook.title
			local_node.sendData("NOTE_MANAGER_UPDATE_NOTEBOOK_RESULT", liveObject)
			GlobalDatabaseHandler.saveSession(dbSession)
			dbSession.close()

		def receivedUserSession(sessionID):
			print("Verifying...")
			userID = getUserBySession(sessionID, dbSession, getPeerIP(local_node))
			if userID != None:
				#Update Notebook
				local_node.fetchDataFromBuffer("NOTE_MANAGER_NOTEBOOK_DETAILS", lambda data: createNotebookPage(data, userID))
			else:
				return
		local_node.fetchDataFromBuffer("NOTE_MANAGER_GET_SESSION_ID", receivedUserSession)
		print("Waiting on user ID")

class Note_Manager_Delete_Notebook(Promise):
	def clientAction(self, **kw):
		"""Takes 2 arguments:
		notebookID: This is the ID of the notebook to be deleted
		func: The function to be executed once the notebook has been updated
		"""
		pass

	def serverAction(self, **kw):
		pass

class Note_Manager_Update_Notebook_Page(Promise):
	def clientAction(self, **kw):
		"""Takes 2 arguments:
		notebookPage: This is the NotebookPage to be updated
		func: The function to be executed once the notebook has been updated
		Returns an updated Notebook object or None"""
		pass

	def serverAction(self, **kw):
		pass

class Note_Manager_Delete_Notebook_Page(Promise):
	def clientAction(self, **kw):
		"""Takes 2 arguments:
		notebookPageID: This is the ID of the NotebookPage to be deleted
		func: The function to be executed once the notebook has been deleted"""
		pass

	def serverAction(self, **kw):
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
Promises.register(Note_Manager_Create_Notebook_Page())
Promises.register(Note_Manager_Update_Notebook())
