from local_api.file.dbobjects import DatabaseBase

from sqlalchemy import Column, Integer, String, DateTime

class Credential(DatabaseBase):
	__tablename__ = "Credential_Manager_Plugin_Credentials"

	id = Column(String(36), primary_key=True)
	username = Column(String)
	password = Column(String)
	target = Column(String)
	notes = Column(String)
	displayName = Column(String)
	permissionID = Column(String(36)) #UUID4 for permission NODE
	createdByID = Column(String(36)) #UserID

class CredentialPermission(DatabaseBase):
	__tablename__ = "Credential_Manager_Plugin_Credential_Permissions"

	id = Column(String(36), primary_key=True)
	credentialPermissionID = Column(String(36)) #Refers to Credential.permissionID
	userID = Column(String(36)) #Refers to User.id
