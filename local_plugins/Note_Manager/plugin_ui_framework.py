from common_ui.atoms import Frame, Entry

class NotebookPanel(Frame):
	__NOTEBOOK_OBJECTS__ = []
	def __init__(self, master, **kw):
		Frame.__init__(self, master, **kw)

class CategorySearchPanel(Frame):
	def __init__(self, master, **kw):
		Frame.__init__(self, master, **kw)

		self.className = "Frame"

		self.searchPanel = SearchPanel(self)
		self.searchPanel.pack(fill="x")

class NoteSearchPanel(Frame):
	def __init__(self, master, **kw):
		Frame.__init__(self, master, **kw)

		self.className = "Frame"

		self.searchPanel = SearchPanel(self)
		self.searchPanel.pack(fill="x")

class SearchPanel(Frame):
	__SEARCH_ACTION__ = None
	__DEFAULT_SEARCH_TEXT__ = ""
	def __init__(self, master, **kw):
		Frame.__init__(self, master, **kw)

		self.className = "Frame"

		self._searchWidget = Entry(self)
		self._searchWidget.className = "SearchPanel_SearchEntry"
		self._searchWidget.pack(fill="x", expand=True, padx=5, pady=5, ipadx=5, ipady=5)

	def getSearchAction(self):
		return self.__SEARCH_ACTION__

	def setSearchAction(self, func):
		self.__SEARCH_ACTION__ = func
