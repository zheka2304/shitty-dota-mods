import os
import os.path
import json
from tkinter import Tk
from tkinter.filedialog import askdirectory 


def steamapps_input():
	Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
	return askdirectory() # show an "Open" dialog box and return the path to the selected file

	
def steamapps_path_validator(path):
	if not os.path.isdir(path):
		print("path is not a directory")
		return False
	if not os.path.isfile(os.path.join(path, "common/dota 2 beta/game/dota/gameinfo.gi")):
		print("steamapps/common/dota 2 beta/game/dota/gameinfo.gi file not found")
		return False
	return True


USER_SETTINGS_FILENAME = "user_settings.json"
USER_SETTINGS_STRUCTURE = {
	"steamapps_path": {
		"query": "Input valid steamapps directory path:",
		"validator": steamapps_path_validator,
		"input": steamapps_input
	}
}

user_settings = {}

if os.path.isfile(USER_SETTINGS_FILENAME):
	with open(USER_SETTINGS_FILENAME, "r") as user_settings_file:
		try:
			user_settings = json.loads(user_settings_file.read())
		except Exception:
			print("failed to read user settings json, recreating settings")

user_settings_modified = False
for key, data in USER_SETTINGS_STRUCTURE.items():
	if key not in user_settings:
		while True:
			value = None
			if "input" in data:
				value = data["input"]()
			else:
				value = input(data["query"])
			if data["validator"](value):
				user_settings_modified = True
				user_settings[key] = value
				break

if user_settings_modified:
	with open(USER_SETTINGS_FILENAME, "w") as user_settings_file:
		user_settings_file.write(json.dumps(user_settings, indent=4))

				
def get_user_settings():
	return user_settings
	
