class PromiseManager:
	def __init__(self):
		self._envVariables = {}
		self._promises = {}
		self._defaultExecutionMode = None

	def addEnvironmentVariable(self, name, var):
		try:
			currentvarVal = self._envVariables[name]
			raise Warning("There is already an environment variable for this promise named %s"%name)
		except KeyError:
			pass
		self._envVariables[name] = var
		print("Added %s"%name)

	def getEnvironmentVariable(self, name):
		try:
			currentvarVal = self._envVariables[name]
		except KeyError:
			raise Warning("There is no envionrment variable for: %s"%name)
		return self._envVariables[name]

	def removeEnvironmentVariable(self, name):
		del self._envVariables[name]

	def register(self, promiseInstance):
		try:
			currentVal = self._promises[promiseInstance.promiseName]
			raise Warning("A promise already exists with the name: %s"%promiseInstance.promiseName)
		except KeyError:
			pass
		self._promises[promiseInstance.promiseName] = promiseInstance
		promiseInstance.setRegister(self)

	def getPromise(self, name):
		try:
			return self._promises[name]
		except:
			raise KeyError()

	def setDefaultMode(self, mode="Client"):
		modeOptions = ["Client", "Server", "CommandLine"]
		if mode not in modeOptions:
			raise Warning("The entered mode (%s) is not a valid mode"%mode)
		self._defaultExecutionMode = mode

	def execute(self, promiseName, **kw):
		if "mode" in kw.keys():
			mode = kw["mode"]
			del kw["mode"]
		else:
			mode = self._defaultExecutionMode
		try:
			if mode == "Client":
				return self.getPromise(promiseName).clientAction(**kw)
			elif mode == "Server":
				return self.getPromise(promiseName).serverAction(**kw)
			elif mode == "CommandLine":
				return self.getPromise(promiseName).commandLineAction(**kw)
		except Warning:
			raise PromiseNotFound("Promise attempted to be called that does not exist (%s)"%promiseName)

class Promise:
	def __init__(self):
		self.promiseName = self.__class__.__name__
		self._register = None

	def setRegister(self, register):
		self._register = register
		print("Registered promise with name: %s"%self.promiseName)

	def getEnvironmentVariable(self, var):
		return self._register.getEnvironmentVariable(var)

	def setEnvironmentVariable(self, name, val):
		self._register.setEnvironmentVariable(name, val)

	def removeEnvironmentVariable(self, name):
		self._register.removeEnvironmentVariable(name)

	def clientAction(self, **kw):
		print("The client action for: %s is not defined"%self.promiseName)

	def serverAction(self, **kw):
		print("The server action for: %s is not defined"%self.promiseName)

	def commandLineAction(self, **kw):
		print("The command line action for: %s is not defined"%self.promiseName)

class PromiseNotFound(Warning):
	pass


Promises = PromiseManager()
