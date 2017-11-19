from local_api.ui.base import Window, Frame, Button, Entry, SizedButton

class CalculatorWindow(Window):
	def __init__(self):
		Window.__init__(self)

		self.bind("<<Close_Window>>", self.close_window)

		self.protocol("WM_DELETE_WINDOW", self.hideWindow)
		self.focus()
		self.hideMenu()

		self.entry = Entry(self)
		self.entry.className = "Calc_Entry"
		self.entry.pack(fill="x", anchor="n", padx=5, pady=5, ipadx=5, ipady=5)

		self.buttons = Frame(self)
		self.buttons.pack()

		self.createButtons()

		self.calculateButton = Button(self, text="Calculate!")
		self.calculateButton.pack(fill="x", anchor="s", padx=5, pady=5, ipadx=5, ipady=5)

		self.bind("<Return>", self.calc)

		self.bind("1", lambda e: self.addInput(1))
		self.bind("2", lambda e: self.addInput(2))
		self.bind("3", lambda e: self.addInput(3))
		self.bind("4", lambda e: self.addInput(4))
		self.bind("5", lambda e: self.addInput(5))
		self.bind("6", lambda e: self.addInput(6))
		self.bind("7", lambda e: self.addInput(7))
		self.bind("8", lambda e: self.addInput(8))
		self.bind("9", lambda e: self.addInput(9))
		self.bind("0", lambda e: self.addInput(0))
		self.bind("+", lambda e: self.addInput("+"))
		self.bind("-", lambda e: self.addInput("-"))
		self.bind("/", lambda e: self.addInput("/"))
		self.bind("*", lambda e: self.addInput("*"))
		self.bind("(", lambda e: self.addInput("("))
		self.bind(")", lambda e: self.addInput(")"))
		self.bind(".", lambda e: self.addInput("."))
		self.bind("<BackSpace>", self.backspace)

		self.justCalculated = False
		self.clearNext = False

	def backspace(self, e):
		length = len(self.entry.get())
		self.entry.delete(length-1, length)

	def addInput(self, val):
		if self.clearNext:
			self.entry.delete(0, "end")
			self.clearNext = False
		if self.focus_get() != self.entry:
			cursor = self.entry.index("insert")
			self.entry.insert(cursor, val)
			self.justCalculated = False

	def calc(self, e):
		try:
			ent = self.entry.get()
			if ent != "":
				answ = eval(ent)
				self.justCalculated = True
				self.entry.delete(0, "end")
				self.entry.insert(0, answ)
		except:
			self.entry.delete(0, "end")
			self.entry.insert(0, "Invalid Syntax.")
			self.clearNext = True

	def createButtons(self):
		row = Frame(self.buttons)
		row.pack(fill="x")
		for i in range(1, 10):
			b = SizedButton(row, text=i, height=50, width=50, command=lambda val=i:self.addInput(val))
			b.className = "Calc_SizedButton"
			b.pack(side="left", fill="both", expand=True, padx=7, pady=7, ipadx=10, ipady=10)
			if i%3 == 0:
				row = Frame(self.buttons)
				row.pack(fill="x", expand=True)


	def close_window(self, e=None):
		self.destroy()
