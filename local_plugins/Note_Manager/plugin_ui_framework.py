from common_ui.atoms import Frame

class NotebookPanel(Frame):
	__NOTEBOOK_OBJECTS__ = []
	def __init__(self, master, **kw):
		Frame.__init__(master, **kw)
