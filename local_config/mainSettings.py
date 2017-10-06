from os import getcwd
from os.path import join
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
