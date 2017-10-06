from common_ui.tkx_bootstrap import createNewTree
from common_config.tkx_default_config import STYLE_CONFIG

def getStyles():
	style = createNewTree()

	style["AppView"]["background"] = STYLE_CONFIG["tertiary_color"]

	style["AppLauncher_Sidebar"]["width"] = 35
	style["AppLauncher_Sidebar"]["background"] = STYLE_CONFIG["secondary_color"]


	#There is a strong need for inheritance.
	style["AppLauncher_Sidebar_Button"]["background"] = STYLE_CONFIG["primary_color"]
	style["AppLauncher_Sidebar_Button"]["foreground"] = STYLE_CONFIG["text_color"]
	style["AppLauncher_Sidebar_Button"]["activebackground"] = STYLE_CONFIG["secondary_color"]
	style["AppLauncher_Sidebar_Button"]["activeforeground"] = STYLE_CONFIG["text_color"]
	style["AppLauncher_Sidebar_Button"]["relief"] = "flat"
	style["AppLauncher_Sidebar_Button"]["height"] = 2

	style["AppLauncher_Sidebar_Button_Image"]["background"] = STYLE_CONFIG["primary_color"]
	style["AppLauncher_Sidebar_Button_Image"]["foreground"] = STYLE_CONFIG["text_color"]
	style["AppLauncher_Sidebar_Button_Image"]["activebackground"] = STYLE_CONFIG["secondary_color"]
	style["AppLauncher_Sidebar_Button_Image"]["activeforeground"] = STYLE_CONFIG["text_color"]
	style["AppLauncher_Sidebar_Button_Image"]["relief"] = "flat"
	style["AppLauncher_Sidebar_Button_Image"]["height"] = 40

	style["AppLauncher_Sidebar_LaunchButton"]["background"] = STYLE_CONFIG["primary_color"]
	style["AppLauncher_Sidebar_LaunchButton"]["foreground"] = STYLE_CONFIG["text_color"]
	style["AppLauncher_Sidebar_LaunchButton"]["activebackground"] = STYLE_CONFIG["secondary_color"]
	style["AppLauncher_Sidebar_LaunchButton"]["activeforeground"] = STYLE_CONFIG["text_color"]
	style["AppLauncher_Sidebar_LaunchButton"]["relief"] = "flat"
	style["AppLauncher_Sidebar_LaunchButton"]["height"] = 2

	#style["AppLauncher_MainFrame"]["background"] = "#00FF00"

	style["Testing_Blue"]["background"] = "#0000FF"

	style["AppLaunchingIcon"]["background"] = STYLE_CONFIG["secondary_color"]
	style["AppLaunchingIcon_Hover"]["background"] = STYLE_CONFIG["primary_color"]

	return style
