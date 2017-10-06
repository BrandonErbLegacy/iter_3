from common_ui.atoms import Window
from sys import platform

###

from local_ui.templates import HomeTemplate

class AppView(Window):
	def __init__(self):
		Window.__init__(self)

		if platform == "win32":
			#Introduce full custom window
			pass
		else:
			#The TK implementation for unix does not allow typing into overridden windows
			#So we do not do a full custom window for unix based OSes
			pass

		self.geometry("560x560")

		self.launcher_frame = HomeTemplate(self)
		self.launcher_frame.pack_propagate(False)
		self.launcher_frame.pack(fill="both", padx=5, pady=5, expand=True)
	
