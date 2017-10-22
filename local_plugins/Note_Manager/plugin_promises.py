from local_api.network.twisted_promises import Promises, Promise
from local_promises.required_promises import AuthenticatePromise
from local_objects.required_objects import Session
from local_api.file.dbobjects import GlobalDatabaseHandler
from getpass import getpass
from uuid import uuid4

from local_plugins.Note_Manager.plugin_objects import Note, NoteCategory, NoteCategory_Note_Relation

class Note_Manager_List_Notes(Promise):
	@AuthenticatePromise
	def clientAction(self, **kw):
		pass

	@AuthenticatePromise
	def serverAction(self, **kw):
		local_node = kw["NODE"]
		pass

class Note_Manager_List_Notes_By_Multiple_Category_ID(Promise):
	#Lists notes with all categories
	pass

class Note_Manager_Create_Note(Promise):
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
