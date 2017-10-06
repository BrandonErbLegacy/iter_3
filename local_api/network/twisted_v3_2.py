from twisted.internet import reactor, protocol
from twisted.internet.protocol import ClientCreator
import pickle

from uuid import uuid4


PORT = 9000
HOST = 'localhost'

global TWISTED_DEFINED_PROMISE_MANAGER

def setTwistedPromiseManager(mgr):
	print(mgr)
	global TWISTED_DEFINED_PROMISE_MANAGER
	TWISTED_DEFINED_PROMISE_MANAGER = mgr


class DataBufferObject:
	_UNIQUE_ID = None
	_GIVEN_ID = None
	_DATA = None
	_RETURN_CALLS = []
	_FINISHED = False
	def __init__(self, id):
		self._GIVEN_ID = id
		self._UNIQUE_ID = uuid4()

		print("Data Buffer created for ID: %s"%self._GIVEN_ID)

	def setData(self, data):
		self._DATA = data

	def getData(self):
		return self._DATA

	def finalizedData(self):
		print("Finalizing return calls (%i calls)"%len(self._RETURN_CALLS))
		for func in self._RETURN_CALLS:
			func(self.getData())
		print("Calls finalized")

	def addReturnCall(self, func):
		self._RETURN_CALLS.append(func)

	def setFinished(self, bool):
		self._FINISHED = bool

class PromiseExecutionProtocol(protocol.Protocol):
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

	def dataReceived(self, data):
		dataType = data[0:1]
		if dataType == self._PROMISE_FLAG:
			promise_id = data[1:].decode("utf-8")
			print("Request to activate: %s"%promise_id)
			print(self)
			self._PROMISE_MANAGER.execute(promise_id, NODE=self)
			print("Executed: %s"%promise_id)
		elif dataType == self._DATA_ID_FLAG:
			data_id = data[1:]
			self._DATA_BUFFER[data_id] = DataBufferObject(data_id)
			print("Received data ID: %s"%data_id)
		elif dataType == self._DATA_CONTENT_FLAG:
			self._DATA_BUFFER[data_id].setData(pickle.loads(data[1:]))
			print("Received pickled data")
		elif dataType == self._DATA_FINISH_FLAG:
			for item in self._EMPTY_RETURN_CALLS.keys():
				if data_id == item:
					self._DATA_BUFFER[data_id].addReturnCall(self._EMPTY_RETURN_CALLS[data_id])
					del self._EMPTY_RETURN_CALLS[data_id]
			self._DATA_BUFFER[data_id].finalizedData()
			self._DATA_BUFFER[data_id].setFinished(True)
			print("Finished packing buffer")

	def sendData(self, id, data):
		name_flag = self._DATA_ID_FLAG+bytes(id.encode(self._DESIRED_ENCODING))
		self.sendRawData(name_flag)
		print("Name flag finished.")
		content_flag = self._DATA_CONTENT_FLAG+bytes(pickle.dumps(data))
		self.sendRawData(content_flag)
		print("Content flag end.")
		finish_flag = self._DATA_FINISH_FLAG
		self.sendRawData(finish_flag)
		print("Send data transaction finish.")

	def sendRawData(self, data):
		self.transport.write(data)
		self.transport.flush()

	def fetchDataFromBuffer(self, id, func):
		if id in self._DATA_BUFFER.keys():
			self._DATA_BUFFER[id].addReturnCall(func)
		else:
			self._EMPTY_RETURN_CALLS[id] = func

	def executeRemotePromise(self, promiseName):
		print("Sending promise activation record: %s"%promiseName)
		promiseName =  bytes("0".encode(self._DESIRED_ENCODING))+bytes(promiseName.encode(self._DESIRED_ENCODING))
		self.sendRawData(promiseName)
		print("Send complete!")


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
