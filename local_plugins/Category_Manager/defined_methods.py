from local_api.plugin.defined_methods import PluginLoader as plgOverload
from local_plugins.Category_Manager.plugin_objects import Category

class PluginLoader(plgOverload):
	def __init__(self, side):
		plgOverload.__init__(self, side)

		self.CONST_PLUGIN_NAME = "Categories"
		self.ON_LOAD_METHOD = self.ON_LOAD_ACTIVE

	def ON_LOAD_ACTIVE(self):
		print("Loaded %s"%self.CONST_PLUGIN_NAME)
