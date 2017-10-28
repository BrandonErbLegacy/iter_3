from common_ui.atoms import Frame, Entry, Label, Button

class NotebookPanel(Frame):
	__NOTEBOOK_OBJECTS__ = []
	def __init__(self, master, **kw):
		Frame.__init__(self, master, **kw)

class CategorySearchPanel(Frame):
	def __init__(self, master, **kw):
		Frame.__init__(self, master, **kw)

		self.className = "Frame"

		self.headingFrame = Frame(self)
		self.headingFrame.pack(side="top", fill="x", padx=5, pady=5)

		self.categoryLabel = Label(self.headingFrame, text="Categories")
		self.categoryLabel.className = "Heading_Label"
		self.categoryLabel.pack(side="left", fill="x", expand=True, anchor="center")

		self.createNewCategoryButton = Button(self.headingFrame, text="+")
		self.createNewCategoryButton.pack(side="right")

		self.searchPanel = SearchPanel(self)
		self.searchPanel.pack(fill="x")

class NoteSearchPanel(Frame):
	def __init__(self, master, **kw):
		Frame.__init__(self, master, **kw)

		self.className = "Frame"

		self.headingFrame = Frame(self)
		self.headingFrame.pack(side="top", fill="x", padx=5, pady=5)

		self.noteLabel = Label(self.headingFrame, text="Notebooks")
		self.noteLabel.className = "Heading_Label"
		self.noteLabel.pack(side="left", fill="x", expand=True, anchor="center")

		self.createNewNotebookButton = Button(self.headingFrame, text="+")
		self.createNewNotebookButton.pack(side="right")

		self.searchPanel = SearchPanel(self)
		self.searchPanel.pack(fill="x")

		self.notebook_frame = Frame(self)
		self.notebook_frame.pack(fill="both", expand=True)

	def add_notebook(self, notebook):
		button = Button(self.notebook_frame, text=notebook.title)
		button["command"] = lambda: self.launchNotebook(notebook)
		button.pack(fill="x", padx=5, pady=1, ipadx=5, ipady=5)

	def launchNotebook(self, notebook):
		print("Launching (%s) notebook with id %s"%(notebook.title, notebook.id))

class SearchPanel(Frame):
	__SEARCH_ACTION__ = None
	__DEFAULT_SEARCH_TEXT__ = ""
	def __init__(self, master, **kw):
		Frame.__init__(self, master, **kw)

		self.className = "Frame"

		self.searchLabel = Label(self, text="Search:")
		self.searchLabel.pack(side="left")

		self._searchWidget = Entry(self)
		self._searchWidget.className = "SearchPanel_SearchEntry"
		self._searchWidget.pack(side="right", fill="x", expand=True, padx=5, pady=5, ipadx=5, ipady=5)

	def getSearchAction(self):
		return self.__SEARCH_ACTION__

	def setSearchAction(self, func):
		self.__SEARCH_ACTION__ = func
