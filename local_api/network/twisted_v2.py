from twisted.internet import reactor, protocol
from twisted.internet.protocol import ClientCreator


PORT = 9000
HOST = 'localhost'

###############
# Actions to implement into protocol:
#  -SendData/ReceiveData
#  -SendPromise/ReceivePromise
#  -Change data handle system to use a buffer
###############

class PromiseExecutionProtocol(protocol.Protocol):
	_STATE = None
	_DATA_BUFFER = {}
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
		data = data[1:]
		print("Data Type: %s"%dataType)
		print("Data: %s"%data)

	def sendData(self, value, isPromise=False):
		print("Sending: %s"%value)
		if isPromise == False:
			value = bytes("0")+value
		self.transport.write(value)
		print("Value has been sent!")

	def executePromise(self, promiseName):
		promiseName =  bytes("1".encode("utf-8"))+promiseName
		self.sendData(promiseName, isPromise=True)


class PromiseExecutionServer(PromiseExecutionProtocol):
	def __init__(self):
		protocol.Protocol.__init__(self)
		self.setState("server")

class PromiseExecutionServerFactory(protocol.Factory):
	protocol = PromiseExecutionServer

class PromiseExecutionClient(PromiseExecutionProtocol):
	def __init__(self):
		protocol.Protocol.__init__(self)
		self.setState("client")

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
