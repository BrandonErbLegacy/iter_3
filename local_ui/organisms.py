from common_ui.atoms import Frame, Button, Label
from tkinter import PhotoImage

class AppLauncherFrame(Frame):
	def __init__(self, master, **kw):
		Frame.__init__(self, master, **kw)
		self.className = "Frame"

		appLauncherLabel = Label(self, text="Installed Applications", font=(16))
		appLauncherLabel.pack(fill="x", anchor="center", pady=5)
		#appLauncherLabel = Label(self, text="", font=(8))
		#appLauncherLabel.pack(fill="x", anchor="center")

	def addAppToLauncher(self, text, icon, action):
		#if icon == None:
		launchingButton = Button(self, text=text, anchor="w")
		#else:
		#	print("%s assigned an image"%text)
		#	launchingButton = Button(self, image=PhotoImage(icon), anchor="w")
		launchingButton["command"] = lambda: action()
		launchingButton.className = "AppLauncher_Sidebar_LaunchButton"
		launchingButton.pack(fill="x", pady=1, padx=2)
