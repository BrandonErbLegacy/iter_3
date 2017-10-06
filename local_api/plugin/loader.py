from local_config.mainSettings import DEFAULT_PLUGIN_DIRECTORY
from local_api.file.filesearch import Search
import importlib.util
import os

class PluginManager:
	def __init__(self, bootstrap=None):
		self.bootstrap = bootstrap
		self.loadedPlugins = []
		self.unloadedPlugins = []

		potentialPlugins = []

		searcher = Search([DEFAULT_PLUGIN_DIRECTORY])
		searcher.setExtensionWhiteList(".py")
		searcher.searchForStringInFile("class PluginLoader")
		results = searcher.getFileListResults()
		self.validatePlugins(results)

	def validatePlugins(self, p):
		for pluginPath in p:
			try:
				try:
					pluginModuleName = pluginPath.split("\\")[-1:][0].split(".")[:-1][0]
					#The above strips down ''\path\to\plugin.py' to be 'plugin'
				except:
					pluginModuleName = pluginPath.split("/")[-1:][0].split(".")[:-1][0]
				pluginModuleSpec = importlib.util.spec_from_file_location(pluginModuleName, pluginPath)
				pluginLoadedModule = importlib.util.module_from_spec(pluginModuleSpec)
				pluginModuleSpec.loader.exec_module(pluginLoadedModule)
				pluginLoaderOfPlugin = pluginLoadedModule.PluginLoader()
				self.loadedPlugins.append(pluginLoaderOfPlugin)

				self.createSafeBindings(pluginLoaderOfPlugin)
			except IOError:
				self.unloadedPlugins.append(pluginPath)

	def createSafeBindings(self, plugin):
		if plugin.ON_FIND_METHOD != None:
			plugin.ON_FIND_METHOD(None)
		if plugin.UI_TREE_STYLES != None:
			if self.bootstrap:
				self.bootstrap.addStyleSheetToExisting(plugin.UI_TREE_STYLES)
