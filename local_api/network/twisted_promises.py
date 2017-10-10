# Twisted Promises:

# Override PromiseManager to take connectProtocol (from twisted_connection_success in main.py)
# PromiseManager.execute() triggers
#  Client --- execute promise --- > Server

from common_api.promises.promises import PromiseManager
from common_api.promises.promises import Promise as oldPromise

class Promise(oldPromise):
	pass

class TwistedPromiseManager(PromiseManager):
	def __init__(self):
		PromiseManager.__init__(self)
		self._execution_ready = False
		self._connected_protocol = None

	def setExecutionStatus(self, bool):
		self._execution_ready = bool

	def setConnectedProtocol(self, protocol):
		self._connected_protocol = protocol

	def sendData(self, id, data):
		if self._connected_protocol != None:
			self._connected_protocol.sendData(id, data)
		else:
			print("There is no connected protocol!")

	def fetchDataFromBuffer(self, id, func):
		if self._connected_protocol != None:
			self._connected_protocol.fetchDataFromBuffer(id, func)
		else:
			print("There is no connected protocol!")

	def executeRemotePromise(self, promiseName):
		if self._connected_protocol != None:
			self._connected_protocol.executeRemotePromise(promiseName)
		else:
			print("There is no connected protocol!")


global Promises
Promises = TwistedPromiseManager()
