import sys
sys.path.insert(0, r"C:\Users\Brandon\OneDrive\xbm_ui")

from local_api.network.twisted_v3 import PromiseExecutionServerFactory, setTwistedPromiseManager
from twisted.internet import reactor
from local_api.plugin.loader import PluginManager

from local_api.network.twisted_promises import Promises

from local_api.network.twisted_classes import PORT, HOST

from local_api.file.dbobjects import DatabaseBase, GlobalDatabaseHandler

from threading import Thread
#Temporary

setTwistedPromiseManager(Promises)
Promises.setDefaultMode("Server")

class Server:
	_IS_RUNNING = True
	def __init__(self):
		self.pluginManager = PluginManager()

		# Create database handling thread
		Thread(target=self.threadedInputHandler).start()
		#

		self.network_launch()

	def threadedInputHandler(self):
		GlobalDatabaseHandler.startDB()
		self.consoleSession = GlobalDatabaseHandler.createNewSession()
		while self._IS_RUNNING:
			user_input = input("Console input: ")
			if (user_input == "\n") or (user_input == ""):
				continue;
			elif (user_input == "exit"):
				self._IS_RUNNING = False
				break
			else:
				print("Executing promise: %s"%user_input)
				Promises.execute(user_input, mode="CommandLine", session=self.consoleSession)
		reactor.stop()

	def network_launch(self):
		self.factory = PromiseExecutionServerFactory()
		reactor.listenTCP(PORT, self.factory)
		reactor.run()

Server()
