from common_ui.atoms import Frame, Entry, Label, Button, Window, Text
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

		self.notebookPageContentHolder = Text(self.contentFrame)
		self.notebookPageContentHolder.pack(fill="both", expand=True)

		self.bind("<<Close_Window>>", self.close_window)

		self.focus()

		self.notebookTabManager.setContentHolder(self.notebookPageContentHolder)
		self.notebookTabManager.setNotebookTitleWidget(self.notebookTitle)

	def addNotebookPage(self, notebookPage):
		print(notebookPage)
		self.notebookTabManager.addNotebookPage(notebookPage)

	def createNewNotebookPage(self):
		pass

	def setNotebookObject(self, notebookObject):
		self.__NOTEBOOK_OBJECT__ = notebookObject
		self.notebookTitle.setNotebookTitle(notebookObject.title)

	def setNotebookPages(self, notebookPageList):
		self.__NOTEBOOK_PAGES__ = notebookPageList
		for page in self.__NOTEBOOK_PAGES__:
			self.addNotebookPage(page)

	def close_window(self, e=None):
		self.destroy()

class NotebookTabManager(Frame):
	__NOTEBOOK_CONTENT_HOLDER__ = None
	__NOTEBOOK_TITLE_WIDGET__ = None
	__LOADED_FIRST__ = False
	def __init__(self, master, **kw):
		Frame.__init__(self, master, **kw)

		self.className = "Frame"

		self.addNotebookPageButton = Button(self, text="+")
		self.addNotebookPageButton.pack(side="bottom", fill="x")

	def setContentHolder(self, contentHolder):
		self.__NOTEBOOK_CONTENT_HOLDER__ = contentHolder

	def setNotebookTitleWidget(self, widget):
		self.__NOTEBOOK_TITLE_WIDGET__ = widget

	def swapToPage(self, widget, page):
		self.__NOTEBOOK_CONTENT_HOLDER__.delete("0.0", "end")
		self.__NOTEBOOK_CONTENT_HOLDER__.insert("0.0", page.content)
		self.__NOTEBOOK_TITLE_WIDGET__.setNotebookPageTitle(page.title)

	def addNotebookPage(self, notebookPage):
		page = Button(self, text=notebookPage.title)
		page["command"] = lambda page=page, v=notebookPage: self.swapToPage(page, v)
		page.pack(side="top", fill="x", pady=1)
		if self.__LOADED_FIRST__ == False:
			page.invoke()
			self.__LOADED_FIRST__ = True

class NotebookTitle(Frame):
	def __init__(self, master, **kw):
		Frame.__init__(self, master, **kw)

		self.className = "Frame"

		self.notebookTitle = SaveOnFocusLeaveEntry(self)
		self.notebookTitle.className = "Notebook_Title"
		self.notebookTitle.pack(side="left", padx=5, pady=5, ipadx=5, ipady=5)
		self.notebookTitle.bind("<<Save_On_Focus_Out>>", self.saveNotebookTitleChange)

		self.notebookTitleSeparator = Label(self, text=":")
		self.notebookTitleSeparator.pack(side="left")

		self.notebookPageTitle = SaveOnFocusLeaveEntry(self)
		self.notebookPageTitle.className = "Notebook_Title"
		self.notebookPageTitle.pack(side="left", fill="x", expand=True, padx=5, pady=5, ipadx=5, ipady=5)
		self.notebookPageTitle.bind("<<Save_On_Focus_Out>>", self.saveNotebookPageTitleChange)

	def setNotebookTitle(self, title):
		self.notebookTitle.delete("0", "end")
		self.notebookTitle.insert("0", title)

	def setNotebookPageTitle(self, title):
		self.notebookPageTitle.delete("0", "end")
		self.notebookPageTitle.insert("0", title)

	def saveNotebookTitleChange(self, event):
		print("Request to save title")

	def saveNotebookPageTitleChange(self, event):
		print("Request to save notebook page title")

class HighlightableEntry(Entry):
	def __init__(self, master, **kw):
		Entry.__init__(self, master, **kw)

		self.className = "Notebook_Title_Entry.Inactive"

		self.bind("<FocusIn>", self._highlightWidget)
		self.bind("<FocusOut>", self._unhighlightWidget)

	def _highlightWidget(self, e):
		self.className = "Notebook_Title_Entry.Active"

	def _unhighlightWidget(self, e):
		self.className = "Notebook_Title_Entry.Inactive"

class SaveOnFocusLeaveEntry(HighlightableEntry):
	def __init__(self, master, **kw):
		HighlightableEntry.__init__(self, master, **kw)
		self.bind("<FocusIn>", self._triggerHighlight)
		self.bind("<FocusOut>", self._triggerUnhighlight)

	def _triggerHighlight(self, e):
		self._highlightWidget(e)

	def _triggerUnhighlight(self, e):
		self.event_generate("<<Save_On_Focus_Out>>")
		self._unhighlightWidget(e)
