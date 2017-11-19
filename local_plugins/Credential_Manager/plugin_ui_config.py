from local_api.ui.base import Style
from local_config.defaultStyles import STYLE_CONFIG

def getStyles():
	credPanel = Style("CredentialPanel")
	credPanelLabel = Style("CredentialPanel.Label")
	credPanelFrame = Style("CredentialPanel.Frame")

	credPanel["bg"] = STYLE_CONFIG["secondary_color"]
	credPanelLabel["bg"] = STYLE_CONFIG["secondary_color"]
	credPanelFrame["bg"] = STYLE_CONFIG["secondary_color"]
