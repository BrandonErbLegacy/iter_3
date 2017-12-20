from local_api.ui.base import Window, Frame

from local_plugins.Note_Manager.plugin_ui_framework import NoteSearchPanel, CategorySearchPanel

from local_api.network.twisted_promises import Promises

class NoteManagerWindow(Window):
	def __init__(self):
		self.__FOCUSED__ = False
		Window.__init__(self)

		self.notehashVal = None

		self.geometry("550x600")

		self.noteSearchPanel = NoteSearchPanel(self)
		self.noteSearchPanel.pack(fill="both", expand=True, side="left")

		self.categorySearchPanel = CategorySearchPanel(self)
		self.categorySearchPanel.pack(fill="y", side="right")

		self.bind("<<Close_Window>>", self.close_window)
		self.bind("<FocusIn>", self.highlighted)
		self.bind("<FocusOut>", self.unhighlighted)

		self.focus()

	def highlighted(self, e=None):
		if self.__FOCUSED__ == False:
			self.__FOCUSED__ = True
			self.reset()
			Promises.execute("Note_Manager_List_Notes", func=self.load_notebook_list)

	def unhighlighted(self, e=None):
		self.__FOCUSED__ = False

	def reset(self):
		self.noteSearchPanel.reset()
		self.categorySearchPanel.reset()

	def load_notebook_list(self, list):
		#print("Loading %i notebooks "%(len(list)))
		for item in list:
			if self.add_notebook(item) == False: break

	def add_notebook(self, notebook):
		try:
			self.noteSearchPanel.add_notebook(notebook)
			return True
		except:
			return False

	def close_window(self, e=None):
		self.destroy()
