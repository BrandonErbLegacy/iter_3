from local_api.network.twisted_promises import Promises, Promise
from local_promises.required_promises import AuthenticatePromise
from local_objects.required_objects import Session
from local_api.file.dbobjects import GlobalDatabaseHandler
from getpass import getpass
from uuid import uuid4

from local_plugins.Credential_Manager.plugin_objects import Credential

class Credential_Manager_Create_Credential(Promise):
	@AuthenticatePromise
	def clientAction(self, username, password, target, notes, displayName):
		#The below triggers the server to execute
		cred = Credential()
		cred.username = username
		cred.password = password
		cred.target = target
		cred.notes = notes
		cred.displayName = displayName
		cred.permissionID = self._register.getEnvironmentVariable("AUTHENTICATION_SESSION_ID")
		print("Sending %s sessionID "%cred.permissionID)
		self._register.sendData("NEW_CREDENTIAL", cred)

	def commandLineAction(self, session):
		raise NotImplemented("This is not intended to be used. It's deprecated")
		print("--")
		username = input("Credential Username: ")
		password = getpass("Credential Password: ")
		target = input("Credential Target: ")
		notes = input("Credential Notes: ")
		displayName = input("Credential display name: ")
		print("Creating credential...")
		newCredential = Credential()
		newCredential.username = username
		newCredential.password = password
		newCredential.target = target
		newCredential.notes = notes
		newCredential.displayName = displayName
		GlobalDatabaseHandler.addObject(newCredential, session)
		GlobalDatabaseHandler.saveSession(session)
		print("--")
		print("Creation success!")

	@AuthenticatePromise
	def serverAction(self, **kw):
		print("Received activation record. Activating...")
		local_node = kw["NODE"]
		session = GlobalDatabaseHandler.createNewSession()
		def fetchData(newCred):
			newCred.id = str(uuid4())
			sessionID = newCred.permissionID
			newCred.permissionID = str(uuid4())
			#Retrieve userID by authentication_id
			try:
				sessionObject = session.query(Session).filter(Session.id == sessionID).one()
				newCred.createdByID = sessionObject.userID
			except:
				print("There was an error processing this command.")
			GlobalDatabaseHandler.addObject(newCred, session)
			GlobalDatabaseHandler.saveSession(session)
		local_node.fetchDataFromBuffer("NEW_CREDENTIAL", fetchData)

class Credential_Manager_Update_Credential(Promise):
	@AuthenticatePromise
	def clientAction(self, **kw):
		cred = kw["credential"]
		if (cred.id != None and len(cred.id) == 36):
			self._register.sendData("UPDATE_CREDENTIAL", cred)
		else:
			cred.permissionID = self._register.getEnvironmentVariable("AUTHENTICATION_SESSION_ID")
			self._register.sendData("UPDATE_CREDENTIAL", cred)

	@AuthenticatePromise
	def serverAction(self, **kw):
		local_node = kw["NODE"]
		session = GlobalDatabaseHandler.createNewSession()
		def updateCred(uCred):
			if (uCred.id == None or len(uCred.id) != 36):
				uCred.id = str(uuid4())
				sessionID = uCred.permissionID
				uCred.permissionID = str(uuid4())
				#Retrieve userID by authentication_id
				try:
					sessionObject = session.query(Session).filter(Session.id == sessionID).one()
					uCred.createdByID = sessionObject.userID
				except:
					print("There was an error processing this command.")
				GlobalDatabaseHandler.addObject(uCred, session)
			else:
				cred = session.query(Credential.id == uCred.id).one()
				cred.username = uCred.username
				cred.password = uCred.password
				cred.displayName = uCred.displayName
				cred.notes = uCred.notes
				cred.target = uCred.target
			GlobalDatabaseHandler.saveSession(session)
		local_node.fetchDataFromBuffer("UPDATE_CREDENTIAL", updateCred)

class Credential_Manager_Get_Credential_ID_List(Promise):
	@AuthenticatePromise
	def clientAction(self, **kw):
		load_data_func = kw["func"]
		def received_data(data):
			load_data_func(data)
		self._register.fetchDataFromBuffer("CREDENTIAL_LIST", received_data)

	@AuthenticatePromise
	def serverAction(self, **kw):
		local_node = kw["NODE"]
		session = GlobalDatabaseHandler.createNewSession()
		# Ideally I'd like to use an existing session per plugin
		#  but the framework just isn't ready for that.
		allCreds = session.query(Credential).all()
		local_node.sendData("CREDENTIAL_LIST", allCreds)


Promises.register(Credential_Manager_Create_Credential())
Promises.register(Credential_Manager_Get_Credential_ID_List())
Promises.register(Credential_Manager_Update_Credential())
