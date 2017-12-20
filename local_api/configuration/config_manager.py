from collections import defaultdict


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


class HotkeyManager:
	__HOTKEYS__ = {}

	def addHotkey(self, hotkey):
		if hotkey.module not in self.__HOTKEYS__.keys():
			self.__HOTKEYS__[hotkey.module] = []
		self.__HOTKEYS__[hotkey.module].append(hotkey)

class Hotkey:
	def __init__(self, module, actionName=None, action=None, modifiers=[], keys=[]):
		self.module = module
		self.actionName = actionName
		self.action = action
		self.modifiers = modifiers
		self.keys = keys

	def getTkBind(self):
		returnStr = "<"
		if self.modifiers != None:
			for modifier in self.modifiers:
				returnStr = returnStr+modifier+"-"

		keyCount = len(self.keys)
		i = 0
		for key in self.keys:
			i = i+1
			if i == keyCount:
				returnStr = returnStr+key+">"
			else:
				returnStr = returnStr+key+"-"
		return returnStr

hotkeyManager = HotkeyManager()
