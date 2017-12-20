from local_plugins.Note_Manager.plugin_ui import NoteManagerWindow
from local_plugins.Note_Manager.plugin_ui_framework import NotebookWindow

import local_plugins.Note_Manager.plugin_promises
from local_api.network.twisted_promises import Promises
from local_plugins.Category_Manager.plugin_ui_framework import CreateNewCategory

class Main:
	def __init__(self):
		pass
	def launchUI(self):
		self.nmw = NoteManagerWindow()
		self.nmw.className = "Window"

		self.nmw.bind("<<Create_New_Notebook>>", lambda e: self.launchNewNotebook())
		self.nmw.bind("<<Create_New_Category>>", lambda e: self.createNewCategory())

	def createNewCategory(self):
		win = CreateNewCategory()
		win.setSuccess(lambda d: self.nmw.refreshCategories())

	def launchNewNotebook(self):

		def create(notebookAndPageTuple):
			notebook, page = notebookAndPageTuple
			nnbw = NotebookWindow()
			nnbw.setNotebookObject(notebook)
			nnbw.setNotebookPages([page])

		Promises.execute("Note_Manager_Create_Notebook", func=create)
