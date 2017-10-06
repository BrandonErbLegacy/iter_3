from common_ui.atoms import Window, Frame

class NoteManagerWindow(Window):
	def __init__(self):
		Window.__init__(self)

		self.bind("<<Close_Window>>", self.close_window)

	def close_window(self, e=None):
		self.destroy()
