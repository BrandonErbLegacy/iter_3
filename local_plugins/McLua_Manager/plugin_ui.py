from local_api.ui.base import Window, Frame, Button, Listbox, Label

class ScriptManagerWindow(Window):
	def __init__(self):
		Window.__init__(self)

		categoryButton = Button(self, text="Category Menu")
		refreshButton = Button(self, text="Refresh")
		listLabel = Label(self, text="New Scripts")
		newList = Listbox(self)

		listLabel.pack(fill="x", anchor="center", padx=5, pady=5)
		newList.pack(fill="both", expand=True, padx=5, pady=5)
		refreshButton.pack(fill="x", padx=5, pady=5)
		categoryButton.pack(fill="x", padx=5, pady=5)

		self.bind("<<Close_Window>>", self.close_window)

	def close_window(self, e=None):
		self.destroy()
