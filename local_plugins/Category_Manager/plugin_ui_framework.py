from local_api.ui.base import Frame, Entry, Label, Button, Window, Text, ScrollableFrame, Menu, PanedWindow, OkCancelDialog
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
