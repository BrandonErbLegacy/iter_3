from collections import defaultdict
from tkinter import Tk

from tkinter import Toplevel
from tkinter import Frame as tkFrame
from tkinter import Label as tkLabel
from tkinter import Text as tkText
from tkinter import Entry as tkEntry
from tkinter import Button as tkButton
from tkinter import Checkbutton as tkCheckbutton
from tkinter import Canvas as tkCanvas
from tkinter import Listbox as tkListbox
from tkinter import Scrollbar

from tkinter import IntVar

config = None

class BaseWidget:
	def __init__(self):
		pass

class Bootstrap:
	def __init__(self, hideRoot=False):
		self.root = Tk()
		self.root.withdraw()

		self.windows = []
		self.styles = StyleTree() #So they can all inherit from a master style

		global config
		config = self
		#This sets a global so all of this mod's code can use the config to reference
		#a value of Bootstrap which is set at runtime

	def loadStyle(self, style):
		self.styles.addStyle(style)

	def clearStyles(self):
		self.styles = StyleTree()

	def getRoot(self):
		return self.root

	def mainloop(self):
		self.root.mainloop()

class WidgetStyleBind:
	def __init__(self, widget):
		self.bindClassName(widget)
		self.applyCurrentStyles(widget)

	def bindClassName(self, widget):
		#This code adds a property named className to
		#When className is updated to a different one, it triggers
		#the style changes to be made
		#http://stackoverflow.com/questions/17330160/how-does-the-property-decorator-work
		#http://stackoverflow.com/questions/1325673/how-to-add-property-to-a-class-dynamically
		def getter(instance):
			return instance._className
		def setter(instance, val):
			instance._className = val
			self.applyCurrentStyles(instance)
		def deleter(instance):
			del instance._className

		widget.__class__.className = property(getter, setter, deleter)


	def applyCurrentStyles(self, widget):
		try:
			className = widget._className
			init = False
		except:
			init = True
			className = widget.__class__.__name__

		style = config.styles.getProcessedStyle(className)
		if style == None:
			style = config.styles.getProcessedStyle("")
		for item in style.keys():
			try:
				widget[item] = style[item]
			except:
				pass

		if init:
			widget._className = className
			#Default to widget.__class__.__name__ if not className is specified.


## Style Definition Code ##

class LinkedNode:
	def __init__(self, data):
		self.data = data
		self.child = None
		self.parent = None
	def setChild(self, child):
		self.child = child
	def getChild(self):
		return self.child
	def setParent(self, parent):
		self.parent = parent
	def getParent(self):
		return self.parent
	def getInfo(self):
		return self.data

class Queue:
	def __init__(self, start=None):
		self._QUEUE_START = None
		self._TOP = None
		self.items = 0
		if start == None:
			self._QUEUE_START = start
		else:
			self._QUEUE_START = LinkedNode(start)
			self._TOP = self._QUEUE_START

	def push(self, item):
		if self._QUEUE_START == None:
			self._QUEUE_START = LinkedNode(item)
			self._TOP = self._QUEUE_START
		else:
			currentTop = self.top()
			newQueueItem = LinkedNode(item)
			currentTop.setChild(newQueueItem)
			newQueueItem.setParent(currentTop)
			self._TOP = newQueueItem
		self.items = self.items+1

	def pop(self):
		if self._QUEUE_START == None:
			raise Warning("Attempted to remove an item from an empty stack")
			return None
		else:
			self.items = self.items-1
			parentNode = self.top()
			self._TOP = parentNode.getParent()
			return parentNode.getInfo()

	def top(self):
		return self._TOP

class Style:
	def __init__(self, name, parent=None, _disable_add=False):
		self._STYLE_NAME = name
		self._CHILDREN = []
		self._STYLE_INFORMATION = {}
		self._PARENT = parent

		if _disable_add == False:
			config.styles.addStyle(self)

	def getChildren(self):
		return self._CHILDREN
	def getName(self):
		return self._STYLE_NAME
	def getParent(self):
		return self._PARENT
	def inheritsFrom(self, name):
		self._PARENT = name
		return self
	def addChild(self, child):
		self._CHILDREN.append(child)

	def hasKey(self, key):
		try:
			key = self._STYLE_INFORMATION[key]
			return True
		except KeyError:
			return False

	def __str__(self):
		returnString = "Style (%s) is a substyle of %s with these options: %s.\nChildren: %s"%(self.getName(),
		self.getParent(), str(self._STYLE_INFORMATION), str(self.getChildren()))
		return returnString

	def __repr__(self):
		return "Style (%s)"%self.getName()

	def __setitem__(self, key, item):
		self._STYLE_INFORMATION[key] = item

	def __getitem__(self, key):
		return self._STYLE_INFORMATION[key]

	def __delitem__(self, key):
		del self._STYLE_INFORMATION[key]

	def __len__(self):
		return len(self._STYLE_INFORMATION)

	def keys(self):
		return self._STYLE_INFORMATION.keys()

class StyleTree:
	_TREE_START = Style("", parent=None, _disable_add=True)
	def __init__(self):
		pass

	def examineStyleBranch(self, styleObject, name):
		#print("Exploring %s looking for %s"%(styleObject.getName(), name))
		if name != styleObject.getName():
			for style in styleObject.getChildren():
				if style.getName() == name:
					return (Queue(), style)
				elif len(style.getChildren()) != 0:
					result = self.examineStyleBranch(style, name)
					if result != None:
						stack, obj = result
						stack.push(style)
						return (stack, obj)
			return None
		else:
			return (Queue(), styleObject)

	def addStyle(self, styleObject):
		if styleObject.getParent() == None:
			self._TREE_START.addChild(styleObject)
		else:
			#print("Adding %s with parent: %s"%(styleObject.getName(), styleObject.getParent()))
			#Get parent and then add as Child
			parentName = styleObject.getParent()
			stack, parentObj = self.getStyleNode(parentName)
			parentObj.addChild(styleObject)


	def getStyleNode(self, styleName):
		result = self.examineStyleBranch(self._TREE_START, styleName)
		if result == None:
			return None
		else:
			return result


	def getProcessedStyle(self, styleName):
		val = self.getStyleNode(styleName)
		if val != None:
			stack, obj = val[0], val[1]
			while stack.items != 0:
				parent = stack.pop()
				#print("Merging %s with %s"%(parent.getName(), obj.getName()))
				for key in parent.keys():
					if obj.hasKey(key) == False:
						#This prevents overriding of children by parent
						obj[key] = parent[key]
			return obj
		else:
			return None

## Overridden Tk widgets ##
class Frame(tkFrame):
	def __init__(self, master, **kw):
		tkFrame.__init__(self, master, **kw)
		WidgetStyleBind(self)

class Label(tkLabel):
	def __init__(self, master, **kw):
		tkLabel.__init__(self, master, **kw)
		WidgetStyleBind(self)

class Text(tkText):
	def __init__(self, master, **kw):
		tkText.__init__(self, master, **kw)
		WidgetStyleBind(self)

class Entry(tkEntry):
	def __init__(self, master, **kw):
		tkEntry.__init__(self, master, **kw)
		WidgetStyleBind(self)

class Button(tkButton):
	def __init__(self, master, **kw):
		tkButton.__init__(self, master, **kw)
		WidgetStyleBind(self)

class Listbox(tkListbox):
	def __init__(self, master, **kw):
		tkListbox.__init__(self, master, **kw)
		WidgetStyleBind(self)

class Canvas(tkCanvas):
	def __init__(self, master, **kw):
		tkCanvas.__init__(self, master, **kw)
		WidgetStyleBind(self)

class Checkbox(tkCheckbutton):
	def __init__(self, master, **kw):
		self.variable = IntVar()

		kw["variable"] = self.variable

		tkCheckbutton.__init__(self, master, **kw)
		WidgetStyleBind(self)

	def setValue(self, val):
		self.variable.set(val)

	def isChecked(self):
		return self.variable.get()

class SizedButton(Button):
	def __init__(self, master, **kw):
		newKw = {}
		if "width" in kw.keys():
			newKw["width"] = kw["width"]
		if "height" in kw.keys():
			newKw["height"] = kw["height"]
		del kw["height"]
		del kw["width"]
		self._host = Frame(master, **newKw)
		Button.__init__(self, self._host, **kw)
	def pack(self, **kw):
		self._host.pack_propagate(False)
		self._host.pack(**kw)
		Button.pack(self, fill="both", expand=True)

class TitledFrame(Frame):
	def __init__(self, master, **kw):
		Frame.__init__(self, master, **kw)

		self.title = Label(self)
		self.title.className = "TitledFrame.Title"
		self.title.pack(fill="x", anchor="center")

	def setTitle(self, text):
		self.title["text"] = text

class HighlightableLabel(Label):
	def __init__(self, master, **kw):
		Label.__init__(self, master, **kw)

		self.className = "HighlightableLabel.Normal"

		self.bind("<Enter>", self.highlight)
		self.bind("<Leave>", self.unhighlight)

	def highlight(self, e):
		self.className = "HighlightableLabel.Active"

	def unhighlight(self, e):
		self.className = "HighlightableLabel.Normal"

class Tabber(Frame):
	def __init__(self, master, **kw):
		Frame.__init__(self, master, **kw)
		self.tabs = {}

		self.tabBar = Frame(self, height=33)
		self.tabBar.pack(fill=X, side=TOP, anchor=N)
		self.tabBar.className = "Tabber_TabBar"

		self.selectedTab = None

		self.selectedUuid = None

	def createNewTab(self, frame, text):
		t = Tab(self.tabBar)
		uuid = t.uuid
		t.updateText(text)
		t.frame = frame
		t.pack(anchor=W, fill=Y, side=LEFT, padx=1, pady=1)

		t.textW.bind("<Button-1>", lambda e: self.swapTabByUuid(uuid))
		t.bind("<Button-1>", lambda e: self.swapTabByUuid(uuid))

		t.closeButton["command"] = lambda: self.deleteTabByUuid(uuid)

		self.tabs[uuid] = t
		return uuid

	def swapTabByUuid(self, uuid):
		tab = self.tabs[uuid]
		if self.selectedTab != None:
			self.selectedTab.forget()
			currentTab = self.tabs[self.selectedUuid]
			currentTab.className = "Tab"
			currentTab.textW.className = "Tabber_TabTitle"
			currentTab.status = "Inactive"
			currentTab.closeButton.className = "Tabber_TabCloseButton_Inactive"
			#print(self.getActiveFrame().IDE_GET_OPENED_FILE())
		self.selectedTab = tab.frame
		self.selectedUuid = uuid
		tab.frame.pack(fill=BOTH, expand=True, ipadx=5, ipady=5)
		tab.textW.className = "Tabber_TabTitle_Active"
		tab.status = "Active"
		tab.closeButton.className = "Tabber_TabCloseButton_Active"
		tab.className = "Tab_Active"

	def deleteTabByUuid(self, uuid):
		tab = self.tabs[uuid]
		del self.tabs[uuid]
		if self.selectedUuid == uuid:
			self.selectedUuid = None
			self.selectedTab.forget()
			self.selectedTab = None
		tab.forget()

	def getActiveTabUuid(self):
		return self.selectedUuid

	def getActiveFrame(self):
		return self.selectedTab

class Window(Toplevel):
	def __init__(self, **kw):
		Toplevel.__init__(self, **kw)
		self.__isMain__ = False
		self.protocol("WM_DELETE_WINDOW", self.closeWindow)
		self.__IsShown__ = True
		WidgetStyleBind(self)

		#self.menu = Menu(self)
		#self.menu.pack(fill=X)

	def destroyWindow(self, e=None):
		self.destroy()

	def toggleHide(self):
		if self.__IsShown__:
			self.hideWindow()
		else:
			self.showWindow()

	def hideWindow(self):
		self.__IsShown__ = False
		self.withdraw()

	def showWindow(self):
		self.__IsShown__ = True
		self.deiconify()

	def hideMenu(self):
		pass
		#self.menu.forget()

	def closeWindow(self):
		self.event_generate("<<Close_Window>>")

class Tab(Frame):
	def __init__(self, master, **kw):
		Frame.__init__(self, master, **kw)
		self.uuid = uuid4()
		self.frame = None
		self.text = "New Tab"

		self.status = "Inactive"

		self.textW = Label(self, text=self.text)
		self.textW.className = "Tabber_TabTitle"
		self.textW.pack(fill=BOTH, padx=5, pady=5, side=LEFT)

		self.closeButton = Button(self, text="x")
		self.closeButton.pack(side=RIGHT, anchor=CENTER)
		self.closeButton.className = "Tabber_TabCloseButton_Inactive"

		self.closeButton.bind("<Enter>", self.closeButtonOnHover)
		self.closeButton.bind("<Leave>", self.closeButtonOnUnhover)

	def closeButtonOnHover(self, e):
		self.closeButton.className = "Tabber_TabCloseButton_Hover"

	def closeButtonOnUnhover(self, e):
		self.closeButton.className = "Tabber_TabCloseButton_%s"%self.status

	def updateText(self, text):
		self.textW["text"] = text
		self.text = text

class ScrollableFrame(Frame):
	def __init__(self, master, **kw):
		Frame.__init__(self, master, **kw)
		self.canvas = Canvas(self)
		self.canvas.pack(side="left", fill="both", expand=True)
		self.scroll = Scrollbar(self)
		#self.scroll.pack(side="right", fill="y")

		self.canvas["yscrollcommand"] = self.scroll.set
		self.scroll["command"] = self.canvas.yview

		self.innerFrame = Frame(self.canvas)
		self.canvas_frame = self.canvas.create_window((0,0), window=self.innerFrame, anchor="nw")

		self.innerFrame.bind("<Configure>", self.frameConfig)
		self.canvas.bind('<Configure>', self.frameWidth)
		#self.bind_all("<MouseWheel>", self.innerScroll)

	def showScrollbar(self, t):
		if t == False:
			self.scroll.forget()
		else:
			self.scroll.pack(side="right", fill="y")

	def frameWidth(self, event):
		canvas_width = event.width
		self.canvas.itemconfig(self.canvas_frame, width=canvas_width)

	def frameConfig(self, event):
		self.canvas["scrollregion"] = self.canvas.bbox("all")
		for item in self.innerFrame.winfo_children():
			item.bind("<MouseWheel>", self.innerScroll)

	def configureScroll(self):
		for item in self.innerFrame.winfo_children():
			item.bind("<MouseWheel>", self.innerScroll)

	def innerScroll(self, event):
		self.canvas.yview_scroll(int(-1*(event.delta/40)), "units")

	def getInner(self):
		return self.innerFrame

## Templates for commonly done things ##

class LoginTemplate(Window):
	def __init__(self, **kw):
		Window.__init__(self, **kw)
		self.bind("<<Close_Window>>", self.destroyWindow)
		self.className = "Window"
		self.geometry("300x120")

		self.userFrame = Frame(self)
		self.passFrame = Frame(self)
		self.buttFrame = Frame(self)
		self.extraFrame = Frame(self)

		self.userFrame.pack(fill="x", expand=True, pady=5, padx=5)
		self.passFrame.pack(fill="x", expand=True, pady=5, padx=5)
		self.buttFrame.pack(fill="x", expand=True, pady=5, padx=5)
		self.extraFrame.pack(fill="x", expand=True, pady=5, padx=5)

		self.userLabel = Label(self.userFrame, text="Username: ", width=12)
		self.userLabel.pack(side="left")
		self.userEntry = Entry(self.userFrame)
		self.userEntry.pack(side="right", fill="x", expand=True, ipadx=5, ipady=3)

		self.passLabel = Label(self.passFrame, text="Password: ", width=12)
		self.passLabel.pack(side="left")
		self.passEntry = Entry(self.passFrame, show="*")
		self.passEntry.pack(side="right", fill="x", expand=True, ipadx=5, ipady=3)

		self.okButton = Button(self.buttFrame, text="Go", command=lambda: self.event_generate("<<Login>>"))
		self.okButton.pack(side="left", fill="x", expand=True, padx=5)
		self.cancelButton = Button(self.buttFrame, text="Cancel", command=lambda: self.event_generate("<<Cancel>>"))
		self.cancelButton.pack(side="right", fill="x", expand=True, padx=5)


		self.userEntry.bind("<Return>", lambda e: self.event_generate("<<Login>>"))
		self.passEntry.bind("<Return>", lambda e: self.event_generate("<<Login>>"))

	def getUsername(self):
		return self.userEntry.get()

	def getPassword(self):
		return self.passEntry.get()

class OkDialog(Window):
	def __init__(self, message, **kw):
		Window.__init__(self, **kw)
		self.bind("<<Close_Window>>", self.destroyWindow)
		self.className = "Window"
		self.geometry("300x100")

		self.label = Label(self, text=message)
		self.label.pack(fill="x", expand=True, anchor="w")

		self.okButton = Button(self, text="Ok", command=self.destroyWindow)
		self.okButton.pack(fill="x", expand=True, padx=5, pady=5)

class OkCancelDialog(Window):
	def __init__(self, message, **kw):
		Window.__init__(self, **kw)
		self.bind("<<Close_Window>>", self.destroyWindow)
		self.className = "Window"
		self.geometry("300x100")

		self.label = Label(self, text=message)
		self.label.pack(fill="x", expand=True, anchor="w")

		self.buttonFrame = Frame(self)
		self.buttonFrame.pack(fill="x", expand=True)

		self.okButton = Button(self.buttonFrame, text="Ok")
		self.okButton.pack(side="left", fill="x", expand=True, padx=5, pady=5)

		self.cancelButton = Button(self.buttonFrame, text="Cancel")
		self.cancelButton.pack(side="right", fill="x", expand=True, padx=5, pady=5)

	def setOkAction(self, callback):
		self.okButton["command"] = callback

	def setCancelAction(self, callback):
		self.cancelButton["command"] = callback

## Context Menu Classes ##

class ContextMenu(Frame):
	def spawn(self, event):
		print("Spawning on top of %s"%(event.widget.className))
