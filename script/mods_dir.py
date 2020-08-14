import os.path
import json
import re

from user_settings import get_user_settings


mods_dir = None

def setup_mods_dir():
	steamapps_dir = get_user_settings()["steamapps_path"]
	gameinfo_file = os.path.join(steamapps_dir, "common/dota 2 beta/game/dota/gameinfo.gi")
	
	gameinfo_contents = None
	with open(gameinfo_file, "r") as f:
		gameinfo_contents = f.read()
	
	for i in range(2):
		# remove old gameinfo modifications
		gameinfo_contents = re.sub("\\s*[a-zA-Z_]+\\s+shitty_mods\\s*", "", gameinfo_contents)
		# add new ones
		modifications = {
			"Game\\s+dota\\s+": "Game    shitty_mods",
			"Mod\\s+dota\\s+": "Mod    shitty_mods",
			"Game_LowViolence\\s+dota_lv\\s+": "Game_LowViolence    shitty_mods"
		}
		for regex, mod in modifications.items():
			match = re.search(regex, gameinfo_contents)
			if match is not None:
				offset = match.span()[0]
				gameinfo_contents = gameinfo_contents[:offset] + "\n" + " " * 24 + mod + "\n" + " " * 24 + gameinfo_contents[offset:]
			else:
				print("failed to modify gameinfo entry:", regex)
		
	with open(gameinfo_file, "w") as f:
		f.write(gameinfo_contents)
	
	global mods_dir
	mods_dir = os.path.join(steamapps_dir, "common/dota 2 beta/game/shitty_mods")
	if not os.path.isdir(mods_dir):
		os.makedirs(mods_dir)
	
	
def get_mods_dir():
	return mods_dir
	

def get_vpk_dir():
	steamapps_dir = get_user_settings()["steamapps_path"]
	return os.path.join(steamapps_dir, "common/dota 2 beta/game/dota/pak01_dir.vpk")
	
	
setup_mods_dir()