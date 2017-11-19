from local_api.ui.base import Style
STYLE_CONFIG = {}

STYLE_CONFIG["text_color"] = "#CCCCCC"
STYLE_CONFIG["primary_color"] = "#333333"
STYLE_CONFIG["secondary_color"] = "#222222"
STYLE_CONFIG["tertiary_color"] = "#111111"
STYLE_CONFIG["quad_color"] = "#121212"
STYLE_CONFIG["empahasis_color"] = "#224099"
STYLE_CONFIG["font"] = ("Consolas", 10)

def do_style(boot):
	baseStyle = boot.styles.getProcessedStyle("")
	baseStyle["foreground"] = STYLE_CONFIG["text_color"]
	baseStyle["background"] = STYLE_CONFIG["tertiary_color"]
	baseStyle["font"] = ("Consolas", 10)

	#frameStyle = Style("Frame")

	#frameStyle["background"] = STYLE_CONFIG["secondary_color"]

	buttonStyle = Style("Button")

	buttonStyle["foreground"] = STYLE_CONFIG["text_color"]
	buttonStyle["background"] = STYLE_CONFIG["primary_color"]
	buttonStyle["activebackground"] = STYLE_CONFIG["secondary_color"]
	buttonStyle["activeforeground"] = STYLE_CONFIG["text_color"]
	buttonStyle["relief"] = "flat"

	labelStyle = Style("Label")
	labelStyle["background"] = STYLE_CONFIG["tertiary_color"]
	labelStyle["foreground"] = STYLE_CONFIG["text_color"]

	checkboxStyle = Style("Checkbox")
	checkboxStyle["background"] = STYLE_CONFIG["primary_color"]
	checkboxStyle["foreground"] = STYLE_CONFIG["text_color"]
	checkboxStyle["selectcolor"] = STYLE_CONFIG["primary_color"]
	checkboxStyle["highlightbackground"] = STYLE_CONFIG["primary_color"]
	checkboxStyle["highlightcolor"] = STYLE_CONFIG["text_color"]
	checkboxStyle["activebackground"] = STYLE_CONFIG["primary_color"]
	checkboxStyle["activeforeground"] = STYLE_CONFIG["text_color"]

	entryStyle = Style("Entry")

	entryStyle["background"] = STYLE_CONFIG["primary_color"]
	entryStyle["foreground"] = STYLE_CONFIG["text_color"]
	entryStyle["insertbackground"] = STYLE_CONFIG["text_color"]
	entryStyle["relief"] = "flat"

	textStyle = Style("Text")

	textStyle["wrap"] = "word"
	textStyle["bg"] = STYLE_CONFIG["tertiary_color"]
	textStyle["fg"] = STYLE_CONFIG["text_color"]
	textStyle["font"] = STYLE_CONFIG["font"]
	textStyle["insertbackground"] = STYLE_CONFIG["text_color"]
	textStyle["tabs"] = "1c"

	listboxStyle = Style("Listbox")

	listboxStyle["background"] = STYLE_CONFIG["quad_color"]
	listboxStyle["foreground"] = STYLE_CONFIG["text_color"]
	listboxStyle["highlightbackground"] = STYLE_CONFIG["primary_color"]
	listboxStyle["highlightcolor"] = STYLE_CONFIG["primary_color"]
	listboxStyle["selectbackground"] = STYLE_CONFIG["empahasis_color"]
	listboxStyle["selectforeground"] = STYLE_CONFIG["text_color"]
	listboxStyle["relief"] = "flat"
	listboxStyle["borderwidth"] = 0

	appViewStyle = Style("AppView")

	appViewStyle["background"] = STYLE_CONFIG["tertiary_color"]

	appLaunchSidebarStyle = Style("AppLauncher_Sidebar")

	appLaunchSidebarStyle["width"] = 35
	appLaunchSidebarStyle["background"] = STYLE_CONFIG["secondary_color"]

	sidebarButtonMain = Style("Sidebar_Button_Main")
	sidebarButtonMain["background"] = STYLE_CONFIG["primary_color"]
	sidebarButtonMain["foreground"] = STYLE_CONFIG["text_color"]
	sidebarButtonMain["activebackground"] = STYLE_CONFIG["secondary_color"]
	sidebarButtonMain["activeforeground"] = STYLE_CONFIG["text_color"]
	sidebarButtonMain["relief"] = "flat"
	sidebarButtonMain["height"] = 2

	sidebarButton = Style("AppLauncher_Sidebar_Button", parent="Sidebar_Button_Main")

	sidebarButtonImage = Style("AppLauncher_Sidebar_Button_Image", parent="Sidebar_Button_Main")
	sidebarButtonImage["height"] = 40

	sidebarButtonLaunchButton = Style("AppLauncher_Sidebar_LaunchButton", parent="Sidebar_Button_Main")


	#There is a strong need for inheritance.
	#style["AppLauncher_Sidebar_Button"]["background"] = STYLE_CONFIG["primary_color"]
	#style["AppLauncher_Sidebar_Button"]["foreground"] = STYLE_CONFIG["text_color"]
	#style["AppLauncher_Sidebar_Button"]["activebackground"] = STYLE_CONFIG["secondary_color"]
	#style["AppLauncher_Sidebar_Button"]["activeforeground"] = STYLE_CONFIG["text_color"]
	#style["AppLauncher_Sidebar_Button"]["relief"] = "flat"
	#style["AppLauncher_Sidebar_Button"]["height"] = 2

	#style["AppLauncher_Sidebar_Button_Image"]["background"] = STYLE_CONFIG["primary_color"]
	#style["AppLauncher_Sidebar_Button_Image"]["foreground"] = STYLE_CONFIG["text_color"]
	#style["AppLauncher_Sidebar_Button_Image"]["activebackground"] = STYLE_CONFIG["secondary_color"]
	#style["AppLauncher_Sidebar_Button_Image"]["activeforeground"] = STYLE_CONFIG["text_color"]
	#style["AppLauncher_Sidebar_Button_Image"]["relief"] = "flat"
	#style["AppLauncher_Sidebar_Button_Image"]["height"] = 40

	#style["AppLauncher_Sidebar_LaunchButton"]["background"] = STYLE_CONFIG["primary_color"]
	#style["AppLauncher_Sidebar_LaunchButton"]["foreground"] = STYLE_CONFIG["text_color"]
	#style["AppLauncher_Sidebar_LaunchButton"]["activebackground"] = STYLE_CONFIG["secondary_color"]
	#style["AppLauncher_Sidebar_LaunchButton"]["activeforeground"] = STYLE_CONFIG["text_color"]
	#style["AppLauncher_Sidebar_LaunchButton"]["relief"] = "flat"
	#style["AppLauncher_Sidebar_LaunchButton"]["height"] = 2

	#style["AppLauncher_MainFrame"]["background"] = "#00FF00"

	#style["Testing_Blue"]["background"] = "#0000FF"

	#style["AppLaunchingIcon"]["background"] = STYLE_CONFIG["secondary_color"]
	#style["AppLaunchingIcon_Hover"]["background"] = STYLE_CONFIG["primary_color"]
