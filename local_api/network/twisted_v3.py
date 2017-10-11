from twisted.internet import reactor, protocol
from twisted.internet.protocol import ClientCreator
from twisted.protocols.basic import NetstringReceiver
import pickle

from uuid import uuid4


PORT = 9000
HOST = 'localhost'

## GLOBAL CONSTANTS


global TWISTED_DEFINED_PROMISE_MANAGER

def setTwistedPromiseManager(mgr):
	global TWISTED_DEFINED_PROMISE_MANAGER
	TWISTED_DEFINED_PROMISE_MANAGER = mgr

class DataBufferObject:
	_UNIQUE_ID = None
	_GIVEN_ID = None
	_DATA = None
	_RETURN_CALLS = []
	_FINISHED = False
	_TYPE = "DATA"
	def __init__(self, id):
		self._GIVEN_ID = id
		self._UNIQUE_ID = uuid4()
		self._RETURN_CALLS = []

		#print("Data Buffer Object created for ID: %s"%self._GIVEN_ID)

	def setData(self, data):
		self._DATA = data

	def getData(self):
		return self._DATA

	def finalizedData(self):
		#print("Finalizing return calls (%i calls)"%len(self._RETURN_CALLS))
		for func in self._RETURN_CALLS:
			func(self.getData())
		#print("Calls finalized")
		self._RETURN_CALLS = []

	def addReturnCall(self, func):
		self._RETURN_CALLS.append(func)

	def setFinished(self, bool):
		self._FINISHED = bool

	def isFinished(self):
		return self._FINISHED

	def setType(self, type="DATA"):
		if type not in ["DATA", "PROMISE"]:
			type = "DATA" #Default to data if not DATA or PROMISE
		else:
			self._TYPE = type

	def isData(self):
		if self._TYPE == "DATA":
			return True
		return False

	def isPromise(self):
		if self._TYPE == "PROMISE":
			return True
		return False

class PromiseExecutionProtocol(NetstringReceiver):
	_STATE = None
	_DATA_BUFFER = {}
	_SERVER_TO_CLIENT_CONNS = []
	_EMPTY_RETURN_CALLS = {}
	_DESIRED_ENCODING = "utf-8"
	_PROMISE_MANAGER = None

	_PROMISE_FLAG = bytes("0".encode(_DESIRED_ENCODING))
	_DATA_ID_FLAG = bytes("1".encode(_DESIRED_ENCODING))
	_DATA_CONTENT_FLAG = bytes("2".encode(_DESIRED_ENCODING))
	_DATA_FINISH_FLAG = bytes("3".encode(_DESIRED_ENCODING))

	def setPromiseManager(self, mgr):
		if mgr == None:
			raise Warning("In order to use this framework, a promise manager must be set.")
		else:
			self._PROMISE_MANAGER = mgr

	def setState(self, state):
		if state == "client":
			self._STATE = "CLIENT"
		elif state == "server":
			self._STATE = "SERVER"
		else:
			raise Warning("Undefined state set on PromiseExecutionProtocol")

	def connectionMade(self):
		if self._STATE == "CLIENT":
			print("Client has connected to server!")
		if self._STATE == "SERVER":
			print("Server has a new client connected!")

	def connectionLost(self, reason):
		print("Lost connection, %s"%reason)

	def stringReceived(self, string):
		dataObject = pickle.loads(string)
		print("Data string ID: %s"%dataObject._GIVEN_ID)
		#print(dataObject._TYPE)
		if dataObject.isData():
			self._DATA_BUFFER[dataObject._GIVEN_ID] = dataObject
			if dataObject._GIVEN_ID in self._EMPTY_RETURN_CALLS.keys():
				for func in self._EMPTY_RETURN_CALLS[dataObject._GIVEN_ID]:
					dataObject.addReturnCall(func)
				self._DATA_BUFFER[dataObject._GIVEN_ID].finalizedData()
			else:
				print("No ID for buffer")
				dataObject.setFinished(True)
				self._DATA_BUFFER[dataObject._GIVEN_ID] = dataObject

			## Data is consumed. Remove data from _DATA_BUFFER and return calls from _EMPTY_RETURN_CALLS
			#del self._DATA_BUFFER[dataObject._GIVEN_ID]
			#if dataObject._GIVEN_ID in self._EMPTY_RETURN_CALLS:
			#	del self._EMPTY_RETURN_CALLS[dataObject._GIVEN_ID]
		elif dataObject.isPromise():
			self._PROMISE_MANAGER.execute(dataObject._GIVEN_ID, NODE=self)

	def sendData(self, id, data=None):
		dataObject = DataBufferObject(id)
		if data != None:
			dataObject.setData(data)
		else:
			dataObject.setType("PROMISE")
		dataToString = pickle.dumps(dataObject)
		self.sendString(dataToString)

	def fetchDataFromBuffer(self, id, func):
		if id in self._DATA_BUFFER.keys():
			self._DATA_BUFFER[id].addReturnCall(func)
			if self._DATA_BUFFER[id].isFinished():
				self._DATA_BUFFER[id].finalizedData()
		else:
			if id in self._EMPTY_RETURN_CALLS.keys():
				self._EMPTY_RETURN_CALLS[id].append(func)
			else:
				self._EMPTY_RETURN_CALLS[id] = [func]


	def executeRemotePromise(self, promiseName):
		self.sendData(promiseName)


class PromiseExecutionServer(PromiseExecutionProtocol):
	def __init__(self):
		protocol.Protocol.__init__(self)
		self.setState("server")
		global TWISTED_DEFINED_PROMISE_MANAGER
		self.setPromiseManager(TWISTED_DEFINED_PROMISE_MANAGER)

class PromiseExecutionServerFactory(protocol.Factory):
	protocol = PromiseExecutionServer

class PromiseExecutionClient(PromiseExecutionProtocol):
	def __init__(self):
		protocol.Protocol.__init__(self)
		self.setState("client")
		global TWISTED_DEFINED_PROMISE_MANAGER
		self.setPromiseManager(TWISTED_DEFINED_PROMISE_MANAGER)

class PromiseExecutionClientFactory(protocol.ReconnectingClientFactory):
	protocol = PromiseExecutionClient
	def buildProtocol(self, address):
		proto = PromiseExecutionServerFactory.buildProtocol(self, address)
		self.connectedProtocol = proto
		return proto

def cbConnected(connectedProtocol):
	connectedProtocol.sendData(b"Test Value 123")

def ebConnectError(reason):
	print("Error")

if __name__ == "__main__":
	mode = input("Would you like to start a (s)erver or (c)lient? ")
	if mode == "s":
		print("Creating server")
		factory = PromiseExecutionServerFactory()
		reactor.listenTCP(PORT, factory)
		reactor.run()
	else:
		if mode != "c":
			print("Undefined, defaulting to client")
		print("Creating client")
		factory = PromiseExecutionClientFactory()
		reactor.connectTCP(HOST, PORT, factory)
		cc = ClientCreator(reactor, PromiseExecutionProtocol)
		whenConnected = cc.connectTCP(HOST, PORT)
		whenConnected.addCallbacks(cbConnected, ebConnectError)
		reactor.run()
