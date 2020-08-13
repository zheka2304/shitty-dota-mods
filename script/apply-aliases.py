import os
import os.path
import vpk
import shutil
import re
import json
import subprocess


aliases_json = input("input aliases json file: ")
with open(aliases_json, "r") as f:
	aliases = json.loads(f.read())
	for alias in aliases:
		origin = alias[0]
		item = alias[1]
	
		out_path = os.path.join(output_dir, vpk_entry)
		out_dir = os.path.dirname(out_path)
		if not os.path.isdir(out_dir):
			os.makedirs(out_dir)
		with open(out_path, "wb") as file:
			file.write(vpk_interface[vpk_entry].read());
