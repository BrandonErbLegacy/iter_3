from local_api.ui.base import Bootstrap, Menu
#from common_api.promises.promises import Promises

from local_api.plugin.loader import PluginManager
from local_api.network.twisted_v3 import PORT, HOST, PromiseExecutionClientFactory, PromiseExecutionProtocol, setTwistedPromiseManager
import local_api.network.twisted_tksupport as tksupport
from local_api.network.twisted_promises import Promises

#from common_ui.templates import LoginTemplate
from local_ui.views import AppView, LoginView

from local_config.defaultStyles import do_style

from twisted.internet import reactor
from twisted.internet.protocol import ClientCreator

import local_promises.required_promises #Just runs the local_promises code

#Import ENV_SETTINGS
from local_config.mainSettings import getSettings

ENV = getSettings("DEV")

### Network Execution Bindings ###

def twisted_connection_error(reason):
	print("There was an error connecting to the server: %s"%reason)

def twisted_connection_success(connectedProtocol):
	Promises.setExecutionStatus(True)
	Promises.setConnectedProtocol(connectedProtocol)
	if ENV["DEBUG"]["ACTIVE"]:
		authenticate(ENV["DEBUG"]["USERNAME"], ENV["DEBUG"]["PASSWORD"])

##################################

def launch_app_view(e=None):
	# Create initial App View
	lv.destroy()
	lt = AppView()
	lt.bind("<<Close_Window>>", lambda e: reactor.stop())
	# Load Plugins
	plg_manage = PluginManager(b)
	for activePlugin in plg_manage.loadedPlugins:
		lt.launcher_frame.addAppToLauncher(activePlugin.CONST_PLUGIN_NAME, None, activePlugin.ON_CLICK_METHOD)

def authenticate(username, password):
	Promises.execute("Iter_3_Authenticate", username=username, password=password,
		success=launch_app_view, fail=lambda: print("Authentication failed."))


Promises.setDefaultMode(mode="Client") #Set the PromiseManager to execute promises on client mode by default
setTwistedPromiseManager(Promises) #Bind the PromiseManager to our twisted protocol
b = Bootstrap()
do_style(b) #Apply styles
tksupport.install(b.getRoot()) # run the Twisted reactor within the root mainloop

lv = LoginView()
lv.bind("<<Login>>", lambda e: authenticate(lv.getUsername(), lv.getPassword()))
lv.bind("<<Close_Window>>", lambda e: reactor.stop())



# Create Twisted network connection

twisted_connection_factory = PromiseExecutionClientFactory()
#reactor.connectTCP(HOST, PORT, twisted_connection_factory)
client_creator = ClientCreator(reactor, PromiseExecutionProtocol)
when_connected = client_creator.connectTCP(ENV["HOST"], ENV["PORT"])
when_connected.addCallbacks(twisted_connection_success, twisted_connection_error)


#Start Reactor & tkinter mainloops (this does both)
reactor.run()
