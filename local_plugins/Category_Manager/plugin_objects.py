from local_api.file.dbobjects import DatabaseBase

from sqlalchemy import Column, Integer, String, DateTime


class Category(DatabaseBase):
	__tablename__ = "Category_Manager_Plugin_Category"

	id = Column(String(36), primary_key=True)
	name = Column(String(36))
	description = Column(String(36))
