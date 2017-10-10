import sys
sys.path.insert(0, r"C:\Users\Brandon\OneDrive\xbm_ui")

from common_ui.tkx_bootstrap import Bootstrap
from common_config.tkx_default_config import getStyles as main_styles
#from common_api.promises.promises import Promises

from local_api.plugin.loader import PluginManager
from local_api.network.twisted_v3 import PORT, HOST, PromiseExecutionClientFactory, PromiseExecutionProtocol, setTwistedPromiseManager
import local_api.network.twisted_tksupport as tksupport
from local_api.network.twisted_promises import Promises

#from common_ui.templates import LoginTemplate
from local_ui.views import AppView, LoginView

from local_config.main_styles import getStyles as local_styles

from twisted.internet import reactor
from twisted.internet.protocol import ClientCreator

import local_promises.required_promises #Just runs the local_promises code


### Network Execution Bindings ###

def twisted_connection_error(reason):
	print("There was an error connecting to the server: %s"%reason)

def twisted_connection_success(connectedProtocol):
	Promises.setExecutionStatus(True)
	Promises.setConnectedProtocol(connectedProtocol)

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
b.loadStyleSheet(main_styles())
b.addStyleSheetToExisting(local_styles)
tksupport.install(b.getRoot()) # run the Twisted reactor within the root mainloop

lv = LoginView()
lv.bind("<<Login>>", lambda e: authenticate(lv.getUsername(), lv.getPassword()))
lv.bind("<<Close_Window>>", lambda e: reactor.stop())


# Create Twisted network connection

twisted_connection_factory = PromiseExecutionClientFactory()
#reactor.connectTCP(HOST, PORT, twisted_connection_factory)
client_creator = ClientCreator(reactor, PromiseExecutionProtocol)
when_connected = client_creator.connectTCP(HOST, PORT)
when_connected.addCallbacks(twisted_connection_success, twisted_connection_error)

#Start Reactor & tkinter mainloops (this does both)
reactor.run()
