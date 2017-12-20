from local_api.file.dbobjects import DatabaseBase

from sqlalchemy import Column, Integer, String, DateTime

class Script(DatabaseBase):
	__tablename__ = "McLua_Manager_Scripts"

	UID = Column(String(36), primary_key=True)
	Contents = Column(String)
	Name = Column(String(80))
	TargetName = Column(String(80))

class CategoryScriptRelation(DatabaseBase):
	__tablename__ = "McLua_Manager_CategoryScriptRelations"

	CategoryUID = Column(String(36), primary_key=True)
	ScriptUID = Column(String(36), primary_key=True)


class Category(DatabaseBase):
	__tablename__ = "McLua_Manager_Category"

	UID = Column(String(36), primary_key=True)
	Name = Column(String(36))
	SaveStamp = Column(String(36))
