from local_api.ui.base import Window, Frame, Listbox, Button
from .plugin_ui_framework import CredentialPanel
from local_api.network.twisted_promises import Promises
from local_ui.atoms import NetworkConnectedWindow


class CredentialManagerWindow(NetworkConnectedWindow):
	def __init__(self):
		Window.__init__(self)

		self.bind("<<Close_Window>>", self.close_window)

		self.leftFrame = Frame(self)
		self.leftFrame.pack(side="left", fill="y", padx=5, pady=5)

		self.listBox = Listbox(self.leftFrame, width=35)
		self.listBox.pack(fill="both", expand=True)

		self.commandButtonFrame = Frame(self.leftFrame)
		self.commandButtonFrame.pack(side="bottom", fill="x", pady=5)

		self.addCredButton = Button(self.commandButtonFrame, text="Add")
		self.addCredButton.pack(fill="x", expand=True, side="left", padx=5)
		self.removeCredButton = Button(self.commandButtonFrame, text="Remove")
		self.removeCredButton.pack(fill="x", expand=True, side="right", padx=5)

		self.rightFrame = Frame(self)
		self.rightFrame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

		self.accInfoPanel = CredentialPanel(self.rightFrame)

		self.accInfoPanel.pack(fill="both")

		self._credentials = {}

		self.listBox.bind("<<ListboxSelect>>", self.loadDisplayedCredential)
		self.accInfoPanel.bind("<<Save_Credential>>", self.saveCredential)
		self.addCredButton["command"] = self.accInfoPanel.resetAllValues

	def saveCredential(self, e=None):
		if self.checkIfCredentialSave():
			cred = self.getCredential()
			Promises.execute("Credential_Manager_Update_Credential", credential=cred)
			if (cred.id != None) and (len(cred.id)== 36):
				#Update the local version
				index = self.listBox.curselection()[0]
				self._credentials[index] = cred
			else:
				self._credentials[len(self._credentials.keys())] = cred
				self.listBox.insert("end", cred.displayName)

	def checkIfCredentialSave(self):
		return self.accInfoPanel.checkIfNeedsToBeSaved()

	def getCredential(self):
		return self.accInfoPanel.retrieveCredentialObject()

	def loadDisplayedCredential(self, e):
		index = self.listBox.curselection()[0]
		credential = self._credentials[index]
		self.accInfoPanel.fillUsingCredentialObject(credential)

	def insertCredentialList(self, credList):
		self._credentials = {}
		self.listBox.delete("0", "end")
		x = 0
		for cred in credList:
			self.listBox.insert("end", cred.displayName)
			self._credentials[x] = cred
			x=x+1

	def close_window(self, e=None):
		self.destroy()
