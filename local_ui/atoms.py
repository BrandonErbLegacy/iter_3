from common_ui.atoms import Frame, Label, Window
from tkinter import StringVar

class AppLaunchingIcon(Frame):
	def __init__(self, master, **kw):
		Frame.__init__(self, master, **kw)

		self.innerFrame = Frame(self, **kw)
		self.innerFrame.className = "Testing_Blue"
		self.innerFrame.pack_propagate(False)
		self.innerFrame.pack(expand=True, fill="both")

		self.textVar = StringVar()

		self.textLabel = Label(self.innerFrame, textvariable=self.textVar)
		self.textLabel.pack(anchor="center", fill="both", expand=True)

		self.textLabel.className = "AppLaunchingIcon"

		self.textLabel.bind("<1>", self.onClick)
		self.textLabel.bind("<Enter>", self.onHover)
		self.textLabel.bind("<Leave>", self.onExit)

	def onHover(self, e):
		self.textLabel.className = "AppLaunchingIcon_Hover"

	def onClick(self, e):
		self.event_generate("<1>")

	def onExit(self, e):
		self.textLabel.className = "AppLaunchingIcon"

	def setText(self, text):
		self.textVar.set(text)

class NetworkConnectedWindow(Window):
	def __init__(self):
		Window.__init__(self)
		#TODO: Add triggers to bind client to discon & recon events

	def network_connection_disconnected(self):
		print("Trigger disconnected window")

	def network_connection_reconnected(self):
		print("Trigger reconnection of window")
