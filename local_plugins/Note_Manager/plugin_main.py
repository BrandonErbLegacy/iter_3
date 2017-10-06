from local_plugins.Note_Manager.plugin_ui import NoteManagerWindow

class Main:
	def __init__(self):
		pass
	def launchUI(self):
		self.cmw = NoteManagerWindow()
		self.cmw.className = "Window"
