from local_api.file.dbobjects import GlobalDatabaseHandler

class PluginLoader:
	#LOCAL_SESSION = GlobalDatabaseHandler.createNewSession()
	def __init__(self, side):
		self.ON_FIND_METHOD = None
		self.ON_LOAD_METHOD = None
		self.ON_CLICK_METHOD = None
		self.ON_DOUBLE_CLICK_METHOD = None
		self.ON_ERROR_METHOD = None
		self.CONST_PLUGIN_NAME = None
		self.UI_TREE_STYLES = None
