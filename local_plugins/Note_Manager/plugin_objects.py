from local_api.file.dbobjects import DatabaseBase

from sqlalchemy import Column, Integer, String, DateTime

class Notebook(DatabaseBase):
	__tablename__ = "Note_Manager_Plugin_Notes"

	id = Column(String(36), primary_key=True)
	createdByID = Column(String(36))
	permissionID = Column(String(36))
	title = Column(String)

class NotebookPage(DatabaseBase):
	__tablename__ = "Note_Manager_Plugin_Notebook_Pages"

	id = Column(String(36), primary_key=True)
	notebook_id = Column(String(36))
	createdByID = Column(String(36))
	permissionID = Column(String(36))
	content = Column(String)
	title = Column(String(5))

class NoteCategory_Note_Relation(DatabaseBase):
	__tablename__ = "Note_Manager_Plugin_Note_Category_relations"

	id = Column(String(36), primary_key=True)
	category_id = Column(String(36))
	note_id = Column(String(36))

class NoteAccess(DatabaseBase):
	__tablename__ = "Note_Manager_Plugin_Note_Access"

	id = Column(String(36), primary_key=True)
	userID = Column(String(36))
	permissionID = Column(String(36))
