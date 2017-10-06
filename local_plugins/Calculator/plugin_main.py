from local_plugins.Calculator.plugin_ui import CalculatorWindow

class Main:
	def __init__(self):
		pass
	def launchUI(self):
		self.cmw = CalculatorWindow()
		self.cmw.className = "Window"
