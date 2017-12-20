from local_plugins.McLua_Manager.plugin_ui import ScriptManagerWindow

AUTH_ID = 'eca44780-8303-41e1-b12a-a2ae300d7590'
#The above is required for every authentication

class Main:
	def __init__(self):
		pass
	def launchUI(self):
		self.cmw = ScriptManagerWindow()
		self.cmw.className = "Window"
