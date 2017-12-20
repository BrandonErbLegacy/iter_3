from local_api.ui.base import Frame, Entry, Label, Button, Window, Text, ScrollableFrame, Menu, PanedWindow, OkCancelDialog, Checkbox
from local_api.configuration.config_manager import Hotkey, hotkeyManager

from local_plugins.Category_Manager.plugin_promises import Promises
from local_plugins.Category_Manager.plugin_objects import Category

class CreateNewCategory(Window):
	def __init__(self, **kw):
		Window.__init__(self, **kw)

		self.successFunction = None

		self.geometry("300x210")

		self.catNameFrame = Frame(self)
		self.catDescFrame = Frame(self)
		self.catButtonsFrame = Frame(self)

		self.catNameFrame.pack(fill="x", padx=5, pady=5)
		self.catDescFrame.pack(fill="x", padx=5)
		self.catButtonsFrame.pack(fill="x", padx=5, pady=5)

		catNameL = Label(self.catNameFrame, text="Category Name")
		self.catNameE = Entry(self.catNameFrame)
		catNameL.pack(fill="x")
		self.catNameE.pack(fill="x", ipadx=5, ipady=5)

		catDescL = Label(self.catDescFrame, text="Category Description")
		self.catDescT = Text(self.catDescFrame, height=5)
		catDescL.pack(fill="x")
		self.catDescT.pack(fill="x", ipadx=5, ipady=5)

		catCreateB = Button(self.catButtonsFrame, text="Create", command=self.create)
		catCancelB = Button(self.catButtonsFrame, text="Cancel", command=self.cancel)
		catCreateB.pack(side="left", fill="x", expand=True, padx=2)
		catCancelB.pack(side="right", fill="x", expand=True, padx=2)

		self.bind("<<Close_Window>>", lambda e: self.destroy())
		self.center()

	def getCatName(self):
		return self.catNameE.get()

	def getCatDesc(self):
		val = self.catDescT.get("0.0", "end")
		if val[:1] == "\n":
			val = val[:-1]
		return val

	def create(self):
		if self.getCatName() == "":
			print("No cat name. Error")
		else:
			cat = Category()
			cat.name = self.getCatName()
			cat.description = self.getCatDesc()
			Promises.execute("Category_Manager_Create_Category", func=self.success, category=cat)

	def setSuccess(self, func):
		self.successFunction = func

	def success(self, returnedCategory):
		if self.successFunction != None:
			self.successFunction(returnedCategory)
		self.destroy()

	def cancel(self):
		self.destroy()

class AddCategoryToNote(Window):
	def __init__(self, **kw):
		Window.__init__(self, **kw)

		self.note = None
		self.executeFunc = None
		self.selectedCats = []
		self.preselectedCats = []

		topFrame = Frame(self)
		self.midFrame = ScrollableFrame(self)
		botFrame = Frame(self)

		topFrame.pack(fill="x", side="top", pady=5)
		self.midFrame.pack(fill="both", expand=True)
		botFrame.pack(fill="x", side="bottom", pady=5)

		topLabel = Label(topFrame, text="Select categories to add")
		topLabel.pack(fill="x")

		successButton = Button(botFrame, text="Add", command=self.save)
		cancelButton = Button(botFrame, text="Cancel", command=self.close_window)

		successButton.pack(side="left", fill="x", padx=5, expand=True)
		cancelButton.pack(side="right", fill="x", padx=5, expand=True)

		self.bind("<<Close_Window>>", self.close_window)

		self.loadAllCategories()

	def loadAllCategories(self):
		Promises.execute("Category_Manager_List_Categories", func=self.inputCategories)

	def preselectCats(self, cList):
		for cat in cList:
			for item in self.midFrame.getInner().winfo_children():
				if item.real_obj.id == cat.category_id:
					item.setValue(True)
		self.preselectedCats = cList

	def inputCategories(self, cList):
		for cat in cList:
			self.addCategory(cat)

	def setSuccessCallback(self, func):
		"""This sets the callback to be executed when the Add button is hit. It will
		pass a list of selected categories to the function when activated,
		as well as self.note"""
		self.executeFunc = func

	def save(self):
		if self.note != None and self.executeFunc != None:
			self.executeFunc(self.selectedCats, self.note)
		self.destroy()

	def setNote(self, note):
		self.note = note
		self.title("Adding categories to %s"%(note.title))
		Promises.execute("Note_Manager_Get_Note_Categories", notebookID=self.note.id, func=self.preselectCats)

	def toggleCat(self, cat):
		if cat in self.selectedCats:
			self.selectedCats.remove(cat)
		else:
			self.selectedCats.append(cat)

	def addCategory(self, cat):
		check = Checkbox(self.midFrame.getInner(), text=cat.name, command=lambda c=cat: self.toggleCat(c), anchor="w")
		check.real_obj = cat
		check.pack(fill="x")

	def close_window(self, e=None):
		self.destroy()
