from twisted.internet import reactor, protocol

PORT = 9000
HOST = 'localhost'

###############

class PromiseExecutionProtocol(protocol.Protocol):
	_STATE = None

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
		print("Received data: %s"%data)

	def sendData(self, value):
		print("You've been received.")

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
	def protocolTriggerPromise(self, promise):
		print("Triggering promise: %s"%promise)
		self.transport.write(promise)


class PromiseExecutionClientFactory(protocol.ReconnectingClientFactory):
	protocol = PromiseExecutionClient

###############

def tester(p):
	print("Hi")


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
		val = reactor.connectTCP(HOST, PORT, factory)
		print(val.protocol)
		reactor.run()
