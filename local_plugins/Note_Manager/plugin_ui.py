from local_api.ui.base import Window, Frame

from local_plugins.Note_Manager.plugin_ui_framework import NoteSearchPanel, CategorySearchPanel

from local_api.network.twisted_promises import Promises
from local_api.configuration.config_manager import Hotkey, hotkeyManager

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

		self.categorySearchPanel.setFilterOnCategoryFunction(self.filterByCat)

		closeWindowHotkey = Hotkey("Note_Manager", actionName="Close Note List Window", modifiers=["Control"], keys=["w"])
		newNoteHotkey = Hotkey("Note_Manager", actionName="Create New Note", modifiers=["Control"], keys=["n"])
		searchHotkey = Hotkey("Note_Manager", actionName="Highlight Search bar", modifiers=["Control"], keys=["s"])
		refreshHotkey = Hotkey("Note_Manager", actionName="Refresh Note selection", modifiers=["Control"], keys=["r"])

		self.bind(closeWindowHotkey.getTkBind(), self.close_window)
		self.bind(newNoteHotkey.getTkBind(), lambda e: self.noteSearchPanel.event_generate("<<Create_New_Notebook>>"))
		self.bind(searchHotkey.getTkBind(), lambda e: self.noteSearchPanel.focusSearch())
		self.bind(refreshHotkey.getTkBind(), lambda e: self.highlighted(e, ignoreFocus=True))

		hotkeyManager.addHotkey(closeWindowHotkey)
		hotkeyManager.addHotkey(newNoteHotkey)
		hotkeyManager.addHotkey(searchHotkey)
		hotkeyManager.addHotkey(refreshHotkey)

		self.bind("<<Close_Window>>", self.close_window)
		self.bind("<FocusIn>", self.highlighted)
		self.bind("<FocusOut>", self.unhighlighted)

		self.focus()

		self.title("Note Manager")

	def filterByCat(self, categories):
		Promises.execute("Note_Manager_List_Notes_By_Multiple_Category_ID", categories=categories, func=self.selectDisplayNotes)

	def selectDisplayNotes(self, notes):
		"""This function displays a subset of existing notes"""
		self.noteSearchPanel.filterNotebooksByIDs(notes)

	def refreshCategories(self, cats):
		Promises.execute("Category_Manager_List_Categories", func=self.displayCategories)

	def displayCategories(self, catList):
		for cat in catList:
			self.categorySearchPanel.addCategory(cat)

	def highlighted(self, e=None, ignoreFocus=False):
		if (self.__FOCUSED__ == False) or (ignoreFocus == True):
			self.__FOCUSED__ = True
			self.reset()
			Promises.execute("Note_Manager_List_Notes", func=self.load_notebook_list)
			Promises.execute("Category_Manager_List_Categories", func=self.displayCategories)

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
