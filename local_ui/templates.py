#from tkinter import PhotoImage
from PIL import Image, ImageTk

from common_ui.atoms import Frame, Button

from local_ui.atoms import AppLaunchingIcon
from local_ui.organisms import AppLauncherFrame

from local_config.mainSettings import DEFAULT_APP_LAUNCHER_ICON_WIDTH, DEFAULT_APP_LAUNCHER_ICON_HEIGHT

class _AppLauncherFrame(Frame):
	def __init__(self, master, **kw):
		Frame.__init__(self, master, **kw)
		self.className = "Frame"
		#self.bind("<Configure>", self.onResize)

		#self._CURRENT_ICONS_PER_ROW = 0
		#self._CURRENT_ICONS_PER_COLUMN = 0

		self._EXISTING_ICONS = []

		#self._COMPUTED_SPOTS = {}

		#self._NEXT_SPOT = (0,0)

		self._GRID_X = 0
		self._GRID_Y = 0

	def createIcon(self, text, method=None):
		print("Creating Icon with text %s"%text)
		iconWidget = AppLaunchingIcon(self, height=DEFAULT_APP_LAUNCHER_ICON_HEIGHT, width=DEFAULT_APP_LAUNCHER_ICON_WIDTH)
		iconWidget.setText(text)
		self._EXISTING_ICONS.append(iconWidget)

		self.placeIcon(iconWidget)

		if method != None:
			iconWidget.bind("<1>", method)

	def placeIcon(self, iconWidget):
		iconWidget.grid(column=self._GRID_X, row=self._GRID_Y, padx=5, pady=5)
		self._GRID_X = self._GRID_X+1
		if self._GRID_X > 5:
			self._GRID_Y = self._GRID_Y+1
			self._GRID_X = 0

	def onResize(self, event):
		#print("Resized to: %i x %i"%(event.width, event.height))
		ICONS_PER_ROW = int(event.width/DEFAULT_APP_LAUNCHER_ICON_WIDTH)
		ICONS_PER_COLUMN = int(event.height/DEFAULT_APP_LAUNCHER_ICON_HEIGHT)
		print("Icons per row %i, Icons per column %i "%(ICONS_PER_ROW, ICONS_PER_COLUMN))

		if ICONS_PER_ROW != self._CURRENT_ICONS_PER_ROW:
			pass


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
