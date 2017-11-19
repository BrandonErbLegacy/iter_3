#from tkinter import PhotoImage
from PIL import Image, ImageTk

from local_api.ui.base import Frame, Button, ScrollableFrame

from local_ui.atoms import AppLaunchingIcon
from local_ui.organisms import AppLauncherFrame

from local_config.mainSettings import DEFAULT_APP_LAUNCHER_ICON_WIDTH, DEFAULT_APP_LAUNCHER_ICON_HEIGHT

class HomeTemplate(Frame):
	## This essentially is V2 of the first launcher
	def __init__(self, master, **kw):
		Frame.__init__(self, master, **kw)
		self.className = "Frame"

		self._currentlySelectedMainFrame = None

		self.sidebarFrame = Frame(self)
		self.sidebarFrame.className = "AppLauncher_Sidebar"
		self.mainFrame = Frame(self)
		self.mainFrame.className = "AppLauncher_MainFrame"

		self.sidebarFrame["width"] = 50
		self.sidebarFrame.pack(side="left", anchor="w", fill="y")

		self.mainFrame.pack_propagate(0)
		self.mainFrame.pack(fill="both", expand=True)

		self.appLauncherFrame = AppLauncherFrame(self.mainFrame)
		#self.helpLauncherFrame =
		#self.hotkeyLauncherFrame =
		#self.configLauncherFrame =

		## Default Sidebar Icons ##
		self.addSidebarIcon("Apps", None, self.appLauncherFrame)
		self.addSidebarIcon("Help", None, None)
		self.addSidebarIcon("Hotkeys", None, None)
		self.addSidebarIcon("Config", r"C:\Users\Brandon\OneDrive\iteration_3\local_assets\settings_small.png", None, side="bottom")

		self._swapMainFrameContext(self.appLauncherFrame)

	def addSidebarIcon(self, text, icon, frame, side="top"):
		if icon == None:
			sidebarButton = Button(self.sidebarFrame, text=text)
			sidebarButton.className = "AppLauncher_Sidebar_Button"
		else:
			print("%s assigned an image"%text)
			img = Image.open(icon)
			imgtk = ImageTk.PhotoImage(img)
			sidebarButton = Button(self.sidebarFrame, image=imgtk)
			sidebarButton.img = imgtk
			sidebarButton.className = "AppLauncher_Sidebar_Button_Image"
		sidebarButton["command"] = lambda: self._swapMainFrameContext(frame)
		sidebarButton.pack(side=side, fill="x", pady=1)

	def _swapMainFrameContext(self, frame):
		print("Swapping to frame.")
		if frame == None:
			print("No frame was passed in!")
			return
		if self._currentlySelectedMainFrame != None:
			self._currentlySelectedMainFrame.forget()
		frame.pack(fill="both", expand=True)
		self._currentlySelectedMainFrame = frame

	def addAppToLauncher(self, text, icon, action=None):
		self.appLauncherFrame.addAppToLauncher(text, icon, action)

	def createIcon(self, text, method=None):
		print("Placeholder for: %s"%text)
