from local_api.ui.base import Frame, Button, Label, ScrollableFrame
from tkinter import PhotoImage

class AppLauncherFrame(Frame):
	def __init__(self, master, **kw):
		Frame.__init__(self, master, **kw)
		self.className = "Frame"

		appLauncherLabel = Label(self, text="Installed Applications", font=(16))
		appLauncherLabel.pack(fill="x", anchor="center", pady=5)

		self.appLauncherScrollable = ScrollableFrame(self)
		self.appLauncherScrollable.pack(fill="both", expand=True)

		#appLauncherLabel = Label(self, text="", font=(8))
		#appLauncherLabel.pack(fill="x", anchor="center")

	def addAppToLauncher(self, text, icon, action):
		#if icon == None:
		launchingButton = Button(self.appLauncherScrollable.getInner(), text=text, anchor="w")
		#else:
		#	print("%s assigned an image"%text)
		#	launchingButton = Button(self, image=PhotoImage(icon), anchor="w")
		launchingButton["command"] = lambda: action()
		launchingButton.className = "AppLauncher_Sidebar_LaunchButton"
		launchingButton.pack(fill="x", pady=1, padx=2)
