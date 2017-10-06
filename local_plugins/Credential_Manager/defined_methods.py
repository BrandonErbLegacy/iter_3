from local_api.plugin.defined_methods import PluginLoader as plgOverload
from local_plugins.Credential_Manager.plugin_main import Main
from local_plugins.Credential_Manager.plugin_ui_config import getStyles

from local_api.network.twisted_promises import Promises


class PluginLoader(plgOverload):
	def __init__(self):
		plgOverload.__init__(self)

		self.runtimePluginClass = Main()

		self.CONST_PLUGIN_NAME = "Credentials"
		self.ON_LOAD_METHOD = self.ON_LOAD_ACTIVE
		self.ON_CLICK_METHOD = self.ON_CLICK_ACTIVE
		self.UI_TREE_STYLES = getStyles()


	def ON_CLICK_ACTIVE(self, event=None):
		self.runtimePluginClass.launchUI()
		Promises.execute("Credential_Manager_Get_Credential_ID_List",
		func=self.runtimePluginClass.fillCredentialPanel)

	def ON_LOAD_ACTIVE(self):
		print("Loaded %s"%self.CONST_PLUGIN_NAME)
		import local_plugins.Credential_Manager.plugin_promises
