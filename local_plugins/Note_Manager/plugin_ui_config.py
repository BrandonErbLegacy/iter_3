from local_api.ui.base import Style
from local_config.defaultStyles import STYLE_CONFIG

def getStyles():

	notebookPanel = Style("NotebookPanel")

	notebookPanel["bg"] = STYLE_CONFIG["secondary_color"]
	notebookPanel["width"] = 200

	#tree["SearchPanel_SearchEntry"]["font"] = (14)

	Style("CategorySearchPanel")["width"] = 400

	Style("Heading_Label")["font"] = (50)

	Style("Notebook_Title")["font"] = (50)

	Style("Notebook_Title_Entry.Active")["background"] = STYLE_CONFIG["secondary_color"]

	Notebook_Title_Entry_Inactive = Style("Notebook_Title_Entry.Inactive")

	Notebook_Title_Entry_Inactive["background"] = STYLE_CONFIG["tertiary_color"]
	Notebook_Title_Entry_Inactive["foreground"] = STYLE_CONFIG["text_color"]
	Notebook_Title_Entry_Inactive["insertbackground"] = STYLE_CONFIG["text_color"]
	Notebook_Title_Entry_Inactive["relief"] = "flat"
