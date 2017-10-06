from common_ui.tkx_bootstrap import createNewTree
from common_config.tkx_default_config import STYLE_CONFIG

def getStyles():
	tree = createNewTree()

	tree["CredentialPanel"]["bg"] = STYLE_CONFIG["secondary_color"]
	tree["CredentialPanel.Label"]["bg"] = STYLE_CONFIG["secondary_color"]
	tree["CredentialPanel.Frame"]["bg"] = STYLE_CONFIG["secondary_color"]

	return tree
