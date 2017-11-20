from os import getcwd
from os.path import join
#from local_api.configuration
ROOT_PROJECT_DIR = getcwd()

DEFAULT_DATA_DIRECTORY = join(ROOT_PROJECT_DIR, "local_storage")
DEFAULT_CONFIG_DIRECTORY = join(ROOT_PROJECT_DIR, "local_config")
DEFAULT_APPLICATION_APIS = join(ROOT_PROJECT_DIR, "local_api")
DEFAULT_SHARED_APPLICATION_APIS = join(ROOT_PROJECT_DIR, "common_api")
DEFAULT_PLUGIN_DIRECTORY = join(ROOT_PROJECT_DIR, "local_plugins")

DEFAULT_PLUGIN_DIRECTORY_STRUCTURE = {
	"local_api":{},
	"local_resources":{},
	"local_objects":{},
	"local_ui":{
		"atoms.py",
		"molecules.py",
		"organisms.py",
		"templates.py",
		"views.py"
	},
}

DEFAULT_APP_LAUNCHER_ICON_WIDTH = 100
DEFAULT_APP_LAUNCHER_ICON_HEIGHT = 100

def getSettings(ENV):
	ENV_SETTINGS = {
		"HOST":"localhost",
		"PORT":9001,
		"DEBUG": {
			"ACTIVE":True,
			"USERNAME":"admin",
			"PASSWORD":"admin"
		}
	}
	if ENV == "PROD":
		ENV_SETTINGS["DEBUG"]["ACTIVE"] = False
		ENV_SETTINGS["HOST"] = "192.168.130.13"
	return ENV_SETTINGS
