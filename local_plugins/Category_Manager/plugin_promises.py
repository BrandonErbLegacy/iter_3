from local_api.network.twisted_promises import Promises, Promise
from local_promises.required_promises import AuthenticatePromise
from local_objects.required_objects import Session
from local_api.file.dbobjects import GlobalDatabaseHandler
from getpass import getpass
from uuid import uuid4

from local_plugins.Category_Manager.plugin_objects import Category

from local_api.helpers.accessControl import getUserBySession, getPeerIP

class Category_Manager_Create_Category(Promise):
	@AuthenticatePromise
	def clientAction(self, **kw):
		"""Takes 2 arguments
		category: The category you wish to create (without an ID)
		func: The function to be executed once it has been created
		"""
		sessionID = self._register.getEnvironmentVariable("AUTHENTICATION_SESSION_ID")
		self._register.sendData("CATEGORY_MANAGER_GET_SESSION_ID", sessionID)
		self._register.sendData("CATEGORY_MANAGER_NEW_CATEGORY", kw["category"])

		self._register.fetchDataFromBuffer("CATEGORY_MANAGER_NEW_CATEGORY", lambda data: kw["func"](data))

	@AuthenticatePromise
	def serverAction(self, **kw):
		local_node = kw["NODE"]
		dbSession = GlobalDatabaseHandler.createNewSession()

		def receivedCategory(userID, category):
			newCatID = str(uuid4())
			category.id = newCatID
			category.userID = userID
			local_node.sendData("CATEGORY_MANAGER_NEW_CATEGORY", category)

			GlobalDatabaseHandler.addObject(category, dbSession)
			GlobalDatabaseHandler.saveSession(dbSession)

			dbSession.close()

		def receivedUserSession(sessionID):
			userID = getUserBySession(sessionID, dbSession, getPeerIP(local_node))
			if userID != None:
				newCatID = str(uuid4())
				local_node.fetchDataFromBuffer("CATEGORY_MANAGER_NEW_CATEGORY", lambda data: receivedCategory(userID, data))
			else:
				return
		local_node.fetchDataFromBuffer("CATEGORY_MANAGER_GET_SESSION_ID", receivedUserSession)

class Category_Manager_List_Categories(Promise):
	@AuthenticatePromise
	def clientAction(self, **kw):
		"""Takes 1 argument
		func: The function to be executed once the notebooks have been listed
		Returns a list of notebooks on the server
		"""
		sessionID = self._register.getEnvironmentVariable("AUTHENTICATION_SESSION_ID")

		self._register.sendData("CATEGORY_MANAGER_GET_SESSION_ID", sessionID)

		self._register.fetchDataFromBuffer("CATEGORY_MANAGER_LIST", lambda data: kw["func"](data))

	@AuthenticatePromise
	def serverAction(self, **kw):
		local_node = kw["NODE"]

		dbSession = GlobalDatabaseHandler.createNewSession()

		def getCatList(sessionID):
			userID = getUserBySession(sessionID, dbSession, getPeerIP(local_node))
			if userID != None:
				cats = dbSession.query(Category).filter(Category.userID == userID).all()
				local_node.sendData("CATEGORY_MANAGER_LIST", cats)
				dbSession.close()
			else:
				return

		local_node.fetchDataFromBuffer("CATEGORY_MANAGER_GET_SESSION_ID", getCatList)

Promises.register(Category_Manager_Create_Category())
Promises.register(Category_Manager_List_Categories())
