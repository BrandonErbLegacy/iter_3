from common_ui.tkx_bootstrap import createNewTree
from common_config.tkx_default_config import STYLE_CONFIG

def getStyles():
	tree = createNewTree()

	tree["NotebookPanel"]["bg"] = STYLE_CONFIG["secondary_color"]
	tree["NotebookPanel"]["width"] = 200

	#tree["SearchPanel_SearchEntry"]["font"] = (14)

	tree["CategorySearchPanel"]["width"] = 400

	tree["Heading_Label"]["font"] = (50)

	tree["Notebook_Title"]["font"] = (50)

	tree["Notebook_Title_Entry.Active"]["background"] = STYLE_CONFIG["secondary_color"]
	tree["Notebook_Title_Entry.Inactive"]["background"] = STYLE_CONFIG["tertiary_color"]
	tree["Notebook_Title_Entry.Inactive"]["foreground"] = STYLE_CONFIG["text_color"]
	tree["Notebook_Title_Entry.Inactive"]["insertbackground"] = STYLE_CONFIG["text_color"]
	tree["Notebook_Title_Entry.Inactive"]["relief"] = "flat"

	return tree
