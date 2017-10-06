from collection import defaultdict


# The defaultdict based Config should possess crud items based on Config
#  items that are ultimately stored in the master.db
#  The items should automatically and seemlessly update in the db when changed/added/etc
#  Default items should also be specified?
#  By using config items this way we can also keep track of what a user can modify
#  In a global configuration window
#  Underlying support may rely on Promises though? May need to rexamine.
class Config(defaultdict):
	def _write_config_to_db(self):
		pass

	def _read_config_from_db(self):
		pass

	def _update_config_item(self):
		pass

	def _export_config_to_json(self):
		pass

	def _import_config_from_json(self):
		pass
