from local_plugins.Credential_Manager.plugin_ui import CredentialManagerWindow
from local_plugins.Credential_Manager.plugin_promises import Credential_Manager_Create_Credential

from local_api.network.twisted_promises import Promises

class Main:
	def __init__(self):
		pass
	def launchUI(self):
		self.cmw = CredentialManagerWindow()
		self.cmw.className = "Window"

	def fillCredentialPanel(self, credentialList):
		self.cmw.insertCredentialList(credentialList)
