from common_ui.atoms import Window, Frame

from local_plugins.Note_Manager.plugin_ui_framework import NoteSearchPanel, CategorySearchPanel

class NoteManagerWindow(Window):
	def __init__(self):
		Window.__init__(self)

		self.geometry("800x400")

		self.noteSearchPanel = NoteSearchPanel(self)
		self.noteSearchPanel.pack(fill="both", expand=True, side="left")

		self.categorySearchPanel = CategorySearchPanel(self)
		self.categorySearchPanel.pack(fill="y",side="right")

		self.bind("<<Close_Window>>", self.close_window)

	def close_window(self, e=None):
		self.destroy()
