from local_api.ui.base import Frame, Label, Entry, Button, TitledFrame, Text
from local_plugins.Credential_Manager.plugin_objects import Credential

class CredentialPanel(TitledFrame):
	def __init__(self, master, **kw):
		TitledFrame.__init__(self, master, **kw)
		self.setTitle("Account Info")

		self.usernameRow = Frame(self)
		self.passwordRow = Frame(self)
		self.targetRow = Frame(self)
		self.displayRow = Frame(self)
		self.descriptionLabelRow = Frame(self)
		self.descriptionTextRow = Frame(self)
		self.saveButtonRow = Frame(self)

		self.usernameRow.className = "CredentialPanel.Frame"
		self.passwordRow.className = "CredentialPanel.Frame"
		self.targetRow.className = "CredentialPanel.Frame"
		self.displayRow.className = "CredentialPanel.Frame"
		self.descriptionLabelRow.className = "CredentialPanel.Frame"
		self.descriptionTextRow.className = "CredentialPanel.Frame"
		self.saveButtonRow.className = "CredentialPanel.Frame"

		self._createLabel(self.usernameRow, "Username: ")
		self._createLabel(self.passwordRow, "Password: ")
		self._createLabel(self.targetRow, "Target: ")
		self._createLabel(self.displayRow, "Display: ")
		self._createLabel(self.descriptionLabelRow, "Description: ")

		self.usernameEntry = Entry(self.usernameRow)
		self.passwordEntry = Entry(self.passwordRow, show="*")
		self.targetEntry = Entry(self.targetRow)
		self.displayEntry = Entry(self.displayRow)
		self.descriptionText = Text(self.descriptionTextRow, height=6)
		self.saveButton = Button(self.saveButtonRow, text="Create", command=lambda: self.event_generate("<<Save_Credential>>"))

		self.usernameEntry.pack(fill="x", pady=5, ipady=3)
		self.passwordEntry.pack(fill="x", pady=5, ipady=3)
		self.targetEntry.pack(fill="x", pady=5, ipady=3)
		self.displayEntry.pack(fill="x", pady=5, ipady=3)
		self.descriptionText.pack(fill="x", pady=5, ipady=3)
		self.saveButton.pack(fill="x", pady=5, ipady=3)

		self.usernameRow.pack(fill="x", padx=5)
		self.passwordRow.pack(fill="x", padx=5)
		self.targetRow.pack(fill="x", padx=5)
		self.displayRow.pack(fill="x", padx=5)
		self.descriptionLabelRow.pack(fill="x", padx=5)
		self.descriptionTextRow.pack(fill="x", padx=5)
		self.saveButtonRow.pack(fill="x", padx=5)

		self.passwordEntry.bind("<Enter>", self.showPassword)
		self.passwordEntry.bind("<Leave>", self.hidePassword)

		self._currentCredential = None

	def _createLabel(self, master, text):
		label = Label(master, text=text, width=10, anchor="w")
		label.className = "CredentialPanel.Label"
		label.pack(side="left")

	def showPassword(self, e):
		self.passwordEntry["show"] = ""

	def hidePassword(self, e):
		self.passwordEntry["show"] = "*"

	def checkIfNeedsToBeSaved(self):
		if self._currentCredential != None:
			lUser = self.usernameEntry.get()
			lPass = self.passwordEntry.get()
			lTarget = self.targetEntry.get()
			lDisplay = self.displayEntry.get()
			lDescription = self.descriptionText.get("0.0", "end").rstrip()

			needsSaved = False
			if lUser != self._currentCredential.username:
				needsSaved = True
			if lPass != self._currentCredential.password:
				needsSaved = True
			if lTarget != self._currentCredential.target:
				needsSaved = True
			if lDisplay != self._currentCredential.displayName:
				needsSaved = True
			if lDescription != self._currentCredential.notes:
				needsSaved = True
			return needsSaved
		else:
			#If no credential is set, then assume this is a new one
			return True

	def fillUsingCredentialObject(self, credential):
		self.usernameEntry.delete("0", "end")
		self.usernameEntry.insert("0", credential.username)
		self.passwordEntry.delete("0", "end")
		self.passwordEntry.insert("0", credential.password)
		self.targetEntry.delete("0", "end")
		self.targetEntry.insert("0", credential.target)
		self.displayEntry.delete("0", "end")
		self.displayEntry.insert("0", credential.displayName)
		self.descriptionText.delete("0.0", "end")
		self.descriptionText.insert("0.0", credential.notes)
		self._currentCredential = credential
		self.saveButton["text"] = "Save"

	def resetAllValues(self):
		self.usernameEntry.delete("0", "end")
		self.passwordEntry.delete("0", "end")
		self.targetEntry.delete("0", "end")
		self.displayEntry.delete("0", "end")
		self.descriptionText.delete("0.0", "end")
		self._currentCredential = None
		self.saveButton["text"] = "Create"

	def retrieveCredentialObject(self):
		if self._currentCredential == None:
			cred = Credential()
		else:
			cred = self._currentCredential
		cred.username = self.usernameEntry.get()
		cred.password = self.passwordEntry.get()
		cred.target = self.targetEntry.get()
		cred.displayName = self.displayEntry.get()
		cred.notes = self.descriptionText.get("0.0", "end").rstrip()
		return cred
