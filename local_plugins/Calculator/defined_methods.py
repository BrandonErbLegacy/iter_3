from local_api.plugin.defined_methods import PluginLoader as plgOverload
from local_plugins.Calculator.plugin_main import Main

class PluginLoader(plgOverload):
	def __init__(self):
		plgOverload.__init__(self)

		self.runtimePluginClass = Main()

		self.CONST_PLUGIN_NAME = "Calculator"
		self.ON_LOAD_METHOD = self.ON_LOAD_ACTIVE
		self.ON_CLICK_METHOD = self.ON_CLICK_ACTIVE


	def ON_CLICK_ACTIVE(self, event=None):
		self.runtimePluginClass.launchUI()

	def ON_LOAD_ACTIVE(self):
		print("Loaded %s"%self.CONST_PLUGIN_NAME)
