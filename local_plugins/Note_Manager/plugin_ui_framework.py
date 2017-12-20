from local_api.ui.base import Frame, Entry, Label, Button, Window, Text, ScrollableFrame, Menu, PanedWindow, OkCancelDialog, Checkbox
from local_api.network.twisted_promises import Promises
from local_api.configuration.config_manager import Hotkey, hotkeyManager

###############################
## NoteManagerWindow Widgets ##
###############################

class CategorySearchPanel(Frame):
	def __init__(self, master, **kw):
		self.CURRENT_CAT_LIST = []
		Frame.__init__(self, master, **kw)

		self.className = "Frame"

		self.headingFrame = Frame(self)
		self.headingFrame.pack(side="top", fill="x", padx=5, pady=5)

		self.categoryLabel = Label(self.headingFrame, text="Categories")
		self.categoryLabel.className = "Heading_Label"
		self.categoryLabel.pack(side="left", fill="x", expand=True, anchor="center")

		self.createNewCategoryButton = Button(self.headingFrame, text="+")
		self.createNewCategoryButton["command"] = lambda: self.event_generate("<<Create_New_Category>>")
		self.createNewCategoryButton.pack(side="right")

		self.searchPanel = SearchPanel(self)
		self.searchPanel.pack(fill="x")

		self.cat_frame = Frame(self)
		self.cat_frame.pack(fill="both", expand=True)

		self.scrollable = ScrollableFrame(self.cat_frame)
		self.scrollable.pack(fill="both", expand=True)
		self.searchPanel.setSearchAction(self.searchCategories)

	def focusSearch(self):
		self.searchPanel._searchWidget.focus()

	def searchCategories(self):
		#TODO: This function needs to be evaluated for efficiency, and depth
		key = self.searchPanel.getSearchedText()
		if key == "":
			for item in self.scrollable.getInner().winfo_children():
				item.destroy()
			for item in self.CURRENT_CAT_LIST:
				self.addCategory(item, new=False)
		else:
			results = []
			for item in self.CURRENT_CAT_LIST:
				if key.lower() in item.name.lower():
					results.append(item)
				if key.lower() in item.description.lower():
					if item not in results:
						results.append(item)
			#Clear existing notebooks
			for item in self.scrollable.getInner().winfo_children():
				item.destroy()

			if len(results) == 0:
				tempLabel = Label(self.scrollable.getInner(), text="There were no categories found\n for that query :(")
				tempLabel.pack()
			else:
				#Display only notebooks that match
				for item in results:
					self.addCategory(item, new=False)

	def addCategory(self, cat, new=True):
		#print("Adding category with name %s"%cat.name)
		if new == True:
			self.CURRENT_CAT_LIST.append(cat)
		c = Checkbox(self.scrollable.getInner(), text=cat.name, justify="left")
		c.pack(fill="x", expand=True, anchor="e")

	def reset(self):
		self.CURRENT_CAT_LIST = []
		for item in self.scrollable.getInner().winfo_children():
			item.destroy()

class NoteSearchPanel(Frame):
	def __init__(self, master, **kw):
		self.CURRENT_NOTEBOOK_LIST = []
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

		self.scrollable = ScrollableFrame(self.notebook_frame)
		self.scrollable.pack(fill="both", expand=True)
		#self.scrollable.showScrollbar(True)

		#Handle searching of notebooks
		self.searchPanel.setSearchAction(self.searchNotebooks)

	def focusSearch(self):
		self.searchPanel._searchWidget.focus()

	def searchNotebooks(self):
		#TODO: This function needs to be evaluated for efficiency, and depth
		key = self.searchPanel.getSearchedText()
		if key == "":
			for item in self.scrollable.getInner().winfo_children():
				item.destroy()
			for item in self.CURRENT_NOTEBOOK_LIST:
				self.add_notebook(item, new=False)
		else:
			results = []
			for item in self.CURRENT_NOTEBOOK_LIST:
				if key.lower() in item.title.lower():
					results.append(item)

			#Clear existing notebooks
			for item in self.scrollable.getInner().winfo_children():
				item.destroy()

			if len(results) == 0:
				tempLabel = Label(self.scrollable.getInner(), text="There were no notebooks found for that query :(")
				tempLabel.pack()
			else:
				#Display only notebooks that match
				for item in results:
					self.add_notebook(item, new=False)


	def reset(self):
		self.CURRENT_NOTEBOOK_LIST = []
		for item in self.scrollable.getInner().winfo_children():
			item.destroy()

	def add_notebook(self, notebook, new=True):
		if new:
			self.CURRENT_NOTEBOOK_LIST.append(notebook)
		button = Button(self.scrollable.getInner(), text=notebook.title)
		button["command"] = lambda: self.launchNotebook(notebook)
		button.pack(fill="x", padx=5, pady=1, ipadx=5, ipady=5)
		self.scrollable.configureScroll()

	def launchNotebook(self, notebook):
		#print("Launching (%s) notebook with id %s"%(notebook.title, notebook.id))
		nnbm = NotebookWindow()
		nnbm.setNotebookObject(notebook)
		Promises.execute("Note_Manager_Get_Notebook_Pages", notebookID=notebook.id,
			func=lambda data: nnbm.setNotebookPages(data))

class SearchPanel(Frame):

	def __init__(self, master, **kw):
		self.__SEARCH_ACTION__ = None
		self.__DEFAULT_SEARCH_TEXT__ = ""
		Frame.__init__(self, master, **kw)

		self.className = "Frame"

		self.searchLabel = Label(self, text="Search:")
		self.searchLabel.pack(side="left")

		self._searchWidget = Entry(self)
		self._searchWidget.className = "SearchPanel_SearchEntry"
		self._searchWidget.pack(side="right", fill="x", expand=True, padx=5, pady=5, ipadx=5, ipady=5)
		self._searchWidget.bind("<KeyRelease>", lambda e: self.getSearchAction()())
		#Get the search action and call it

	def getSearchedText(self):
		return self._searchWidget.get()

	def clear(self):
		self._searchWidget.delete(0, "END")

	def getSearchAction(self):
		if self.__SEARCH_ACTION__ == None:
			raise Warning("Attempted to search without a search function set.")
		return self.__SEARCH_ACTION__

	def setSearchAction(self, func):
		self.__SEARCH_ACTION__ = func

###############################
##  Notebook Window Widgets  ##
###############################

class NotebookWindow(Window):
	def __init__(self):
		self.__NOTEBOOK_OBJECT__ = None
		self.__NOTEBOOK_PAGES__ = None
		self.__NEEDS_SAVING__ = False
		Window.__init__(self)

		self.geometry("800x400")

		self.menu = Menu(self)
		self.menu.addMainMenu("File")
		self.menu.addSubMenu("File", "New", self.createNewNotebookPage)
		self.menu.addSubMenu("File", "Save", func=self.saveNotebookPage)
		self.menu.pack(fill="x")

		self.panedWindow = PanedWindow(self)
		self.panedWindow.pack(fill="both", expand=True)

		self.notebookTabManager = NotebookTabManager(self.panedWindow)
		self.notebookTabManager.pack(side="left", fill="y")

		self.contentFrame = Frame(self.panedWindow)
		self.contentFrame.pack(side="right", fill="both", expand=True)

		self.notebookTitle = NotebookTitle(self.contentFrame)
		self.notebookTitle.pack(side="top", fill="x", padx=5, pady=5)

		self.notebookPageContentHolder = Text(self.contentFrame)
		self.notebookPageContentHolder.pack(fill="both", expand=True)
		self.notebookPageContentHolder.bind("<KeyRelease>", lambda e: self.setSaved(False))

		self.bind("<<Close_Window>>", self.close_window)
		self.bind("<<Create_New_Notebook_Page>>", self.createNewNotebookPage)
		self.notebookTabManager.bind("<<Swapping_Page>>", self.saveNotebookPage)

		self.focus()

		self.notebookTabManager.setContentHolder(self.notebookPageContentHolder)
		self.notebookTabManager.setNotebookTitleWidget(self.notebookTitle)

		self.panedWindow.add(self.notebookTabManager)
		self.panedWindow.add(self.contentFrame)
		saveHotkey = Hotkey("Note_Manager", actionName="Save", modifiers=["Control"], keys=["s"])
		closeHotkey = Hotkey("Note_Manager", actionName="Close", modifiers=["Control"], keys=["w"])

		self.bind(saveHotkey.getTkBind(), self.saveNotebookPage)
		self.bind(closeHotkey.getTkBind(), self.close_window)

		hotkeyManager.addHotkey(saveHotkey)
		hotkeyManager.addHotkey(closeHotkey)

	def setSaved(self, bool):
		"""True for has been saved. False for has not"""
		self.__NEEDS_SAVING__ = (True if bool == False else False)

	def searchNotebook(self):
		pass

	def addNotebookPage(self, notebookPage):
		self.notebookTabManager.addNotebookPage(notebookPage)

	def createNewNotebookPage(self, e=None):
		notebookDialog = CreateNewNotebookPageWindow()
		notebookDialog.bind("<<Generate_Notebook_Page>>", lambda e: self.execute_createNotebookPage(notebookDialog, self.__NOTEBOOK_OBJECT__.id))
		notebookDialog.bind("<<Close_Window>>", lambda e: notebookDialog.destroy())

	def execute_createNotebookPage(self, notebookDialog, notebookID):
		title = notebookDialog.getNotebookName()
		print("Creating new notebook page: %s"%title)
		Promises.execute("Note_Manager_Create_Notebook_Page", func=lambda data: self.addNotebookPage(data),
			notebookTitle=title, notebookID=notebookID)
		notebookDialog.closeWindow()

	def setNotebookObject(self, notebookObject):
		self.__NOTEBOOK_OBJECT__ = notebookObject
		self.notebookTitle.setNotebookTitle(notebookObject.title)
		self.notebookTitle.updateNotebookObj(notebookObject)

	def setNotebookPages(self, notebookPageList):
		self.__NOTEBOOK_PAGES__ = notebookPageList
		for page in self.__NOTEBOOK_PAGES__:
			self.addNotebookPage(page)

	def saveNotebookPage(self, e=None):

		page = self.notebookTabManager.getCurrentPage()
		if page == None:
			return
		page.content = self.notebookTabManager.getContent()
		Promises.execute("Note_Manager_Update_Notebook_Page", notebookObj=page,
		func=lambda data: print("saved"))

	def needsSaved(self):
		return self.__NEEDS_SAVING__

	def close_window(self, e=None):
		if self.needsSaved():
			def destroyWin():
				self.destroy()
				okCancel.destroy()
			def saveData():
				self.saveNotebookPage()
				self.destroy()
				destroyWin()

			okCancel = OkCancelDialog("Do you want to save this page before exiting?")
			okCancel.setCancelAction(destroyWin)
			okCancel.setOkAction(saveData)
			okCancel.setCancelText("Don't save")
			okCancel.setOkText("Save")
		else:
			self.destroy()

class NotebookTabManager(Frame):
	def __init__(self, master, **kw):
		self.__NOTEBOOK_CONTENT_HOLDER__ = None
		self.__NOTEBOOK_TITLE_WIDGET__ = None
		self.__LOADED_FIRST__ = False
		self.__CURRENT_PAGE__ = None
		Frame.__init__(self, master, **kw)

		self.className = "Frame"

		#self.addNotebookPageButton = Button(self, text="+", command=self.createNewNotebookPage)
		#self.addNotebookPageButton.pack(side="bottom", fill="x")

	def createNewNotebookPage(self, e=None):
		self.event_generate("<<Create_New_Notebook_Page>>")

	def setContentHolder(self, contentHolder):
		self.__NOTEBOOK_CONTENT_HOLDER__ = contentHolder

	def setNotebookTitleWidget(self, widget):
		self.__NOTEBOOK_TITLE_WIDGET__ = widget

	def getCurrentPage(self):
		return self.__CURRENT_PAGE__

	def getContent(self):
		return self.__NOTEBOOK_CONTENT_HOLDER__.get("0.0", "end")

	def swapToPage(self, widget, page):
		self.event_generate("<<Swapping_Page>>")
		self.__NOTEBOOK_CONTENT_HOLDER__.delete("0.0", "end")
		self.__NOTEBOOK_CONTENT_HOLDER__.insert("0.0", page.content)
		self.__NOTEBOOK_TITLE_WIDGET__.updateNotebookPage(page, widget)
		self.__CURRENT_PAGE__ = page

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

		self._notebookTitle = None
		self._notebookPageTitle = None
		self.__NOTEBOOK_OBJECT__ = None
		self.__CURRENT_NOTEBOOK_PAGE__ = None
		self.__CURRENT_NOTEBOOK_WIDGET = None

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
		self._notebookTitle = title

	def setNotebookPageTitle(self, title):
		self.notebookPageTitle.delete("0", "end")
		self.notebookPageTitle.insert("0", title)
		self._notebookPageTitle = title

	def saveNotebookTitleChange(self, event):
		if self._notebookTitle != self.notebookTitle.get():
			self.__NOTEBOOK_OBJECT__.title = self.notebookTitle.get()
			Promises.execute("Note_Manager_Update_Notebook", notebookObj=self.__NOTEBOOK_OBJECT__,
			func=self.updateNotebookObj)

	def saveNotebookPageTitleChange(self, event):
		if self._notebookPageTitle != self.notebookPageTitle.get():
			self.__CURRENT_NOTEBOOK_PAGE__.title = self.notebookPageTitle.get()
			Promises.execute("Note_Manager_Update_Notebook_Page", notebookObj=self.__CURRENT_NOTEBOOK_PAGE__,
			func=self.updateNotebookPage)

	def updateNotebookObj(self, notebookObject):
		self.__NOTEBOOK_OBJECT__ = notebookObject
		self.setNotebookTitle(notebookObject.title)

	def updateNotebookPage(self, notebookPage, widget=None):
		self.__CURRENT_NOTEBOOK_PAGE__ = notebookPage
		self.setNotebookPageTitle(notebookPage.title)
		if widget:
			self.__CURRENT_NOTEBOOK_WIDGET = widget
		if self.__CURRENT_NOTEBOOK_WIDGET:
			self.__CURRENT_NOTEBOOK_WIDGET["text"] = notebookPage.title

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

class CreateNewNotebookPageWindow(Window):
	def __init__(self):
		Window.__init__(self)

		self.className = "Window"

		self.geometry("200x100")

		self.nameLabel = Label(self, text="Name")
		self.nameEntry = Entry(self)

		self.nameLabel.pack(fill="x", padx=5, pady=5)
		self.nameEntry.pack(fill="x", padx=5, ipadx=5, ipady=5)

		self.buttonFrame = Frame(self)
		self.buttonFrame.pack(fill="x", padx=5, pady=5)

		self.okButton = Button(self, text="Create!", command=lambda: self.event_generate("<<Generate_Notebook_Page>>"))
		self.cancelButton = Button(self, text="Cancel", command=lambda: self.destroy())

		self.okButton.pack(side="left", fill="x", expand=True, padx=5)
		self.cancelButton.pack(side="right", fill="x", expand=True, padx=5)

	def getNotebookName(self):
		return self.nameEntry.get();
