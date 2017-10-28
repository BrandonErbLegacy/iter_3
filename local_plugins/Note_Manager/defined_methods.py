from local_api.plugin.defined_methods import PluginLoader as plgOverload
from local_plugins.Note_Manager.plugin_main import Main
from local_plugins.Note_Manager.plugin_ui_config import getStyles

class PluginLoader(plgOverload):
	def __init__(self):
		plgOverload.__init__(self)

		self.runtimePluginClass = Main()

		self.CONST_PLUGIN_NAME = "Notes"
		self.ON_LOAD_METHOD = self.ON_LOAD_ACTIVE
		self.ON_CLICK_METHOD = self.ON_CLICK_ACTIVE
		self.UI_TREE_STYLES = getStyles()

	def ON_CLICK_ACTIVE(self, event=None):
		self.runtimePluginClass.launchUI()

	def ON_LOAD_ACTIVE(self):
		print("Loaded %s"%self.CONST_PLUGIN_NAME)
