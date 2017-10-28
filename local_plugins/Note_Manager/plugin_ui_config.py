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

	return tree
