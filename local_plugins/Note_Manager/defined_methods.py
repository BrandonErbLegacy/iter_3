from local_api.plugin.defined_methods import PluginLoader as plgOverload
from local_plugins.Note_Manager.plugin_main import Main
from local_plugins.Note_Manager.plugin_ui_config import getStyles
from local_api.configuration.config_manager import Hotkey

class PluginLoader(plgOverload):
	def __init__(self, side):
		plgOverload.__init__(self, side)

		self.runtimePluginClass = Main()

		self.CONST_PLUGIN_NAME = "Notes"
		self.ON_LOAD_METHOD = self.ON_LOAD_ACTIVE

		hotkey = Hotkey("Note_Manager", actionName="Launch Notes from Home", action=self.ON_CLICK_ACTIVE,
			modifiers=[], keys=["n"])

		self.LAUNCH_HOTKEY = hotkey

		self.ON_CLICK_METHOD = self.ON_CLICK_ACTIVE
		if side == "client":
			self.UI_TREE_STYLES = getStyles()

	def ON_CLICK_ACTIVE(self, event=None):
		self.runtimePluginClass.launchUI()

	def ON_LOAD_ACTIVE(self):
		print("Loaded %s"%self.CONST_PLUGIN_NAME)
