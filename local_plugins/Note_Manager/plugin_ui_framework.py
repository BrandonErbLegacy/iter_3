from common_ui.atoms import Frame, Entry, Label, Button, Window
from local_api.network.twisted_promises import Promises

###############################
## NoteManagerWindow Widgets ##
###############################

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
		self.createNewNotebookButton["command"] = lambda: self.event_generate("<<Create_New_Notebook>>")
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
		#print("Launching (%s) notebook with id %s"%(notebook.title, notebook.id))
		nnbm = NotebookWindow()
		nnbm.setNotebookObject(notebook)
		Promises.execute("Note_Manager_Get_Notebook_Pages", notebookID=notebook.id,
			func=lambda data: nnbm.setNotebookPages(data))

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

###############################
##  Notebook Window Widgets  ##
###############################

class NotebookWindow(Window):
	__NOTEBOOK_OBJECT__ = None
	__NOTEBOOK_PAGES__ = None
	def __init__(self):
		Window.__init__(self)

		self.geometry("800x400")

		self.notebookTabManager = NotebookTabManager(self)
		self.notebookTabManager.pack(side="left", fill="y")

		self.contentFrame = Frame(self)
		self.contentFrame.pack(side="right", fill="both", expand=True)

		self.notebookTitle = NotebookTitle(self.contentFrame)
		self.notebookTitle.pack(side="top", fill="x", padx=5, pady=5)

		self.bind("<<Close_Window>>", self.close_window)

		self.focus()


	def addNotebookPage(self, notebookPage):
		self.notebookTabManager.addNotebookPage(notebookPage)

	def createNewNotebookPage(self):
		pass

	def setNotebookObject(self, notebookObject):
		self.__NOTEBOOK_OBJECT__ = notebookObject

	def setNotebookPages(self, notebookPageList):
		self.__NOTEBOOK_PAGES__ = notebookPageList
		for page in self.__NOTEBOOK_PAGES__:
			self.addNotebookPage(page)

	def close_window(self, e=None):
		self.destroy()


class NotebookTabManager(Frame):
	def __init__(self, master, **kw):
		Frame.__init__(self, master, **kw)

		self.className = "Frame"

		self.addNotebookPageButton = Button(self, text="+")
		self.addNotebookPageButton.pack(side="bottom", fill="x")

	def addNotebookPage(self, notebookPage):
		page = Button(self, text=notebookPage.title)
		page.pack(side="top")

class NotebookTitle(Frame):
	def __init__(self, master, **kw):
		Frame.__init__(self, master, **kw)

		self.className = "Frame"

		self.notebookTitle = Entry(self)
		self.notebookTitle.className = "Notebook_Title"
		self.notebookTitle.pack(side="left", padx=5, pady=5, ipadx=5, ipady=5)

		self.notebookTitleSeparator = Label(self, text=":")
		self.notebookTitleSeparator.pack(side="left")

		self.notebookPageTitle = Entry(self)
		self.notebookPageTitle.className = "Notebook_Title"
		self.notebookPageTitle.pack(side="left", fill="x", expand=True, padx=5, pady=5, ipadx=5, ipady=5)

	def setNotebookTitle(self, title):
		self.notebookTitle.delete("0.0", "end")
		self.notebookTitle.insert("0.0", title)

	def setNotebookPageTitle(self, title):
		self.notebookPageTitle.delete("0.0", "end")
		self.notebookPageTitle.insert("0.0", title)
