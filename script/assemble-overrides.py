import os
import os.path
import vpk
import shutil
import re
import json
import subprocess
import struct	

from mods_dir import get_mods_dir, get_vpk_dir
from mutagen.mp3 import MP3


globals = {
	"vpk": None,
	"default_sound_header": None
}



def remove_temp_dirs():	
	if os.path.isdir(".temp"):
		shutil.rmtree(".temp")
	if os.path.isdir("vpk/pak01_dir"):
	 	shutil.rmtree("vpk/pak01_dir")
	os.makedirs("vpk/pak01_dir")

		
def set_vpk_path(path):
	globals["vpk"] = vpk.open(path)
		
		
def get_path(path):
	target_file = os.path.join(".temp", path)
	target_dir = os.path.dirname(target_file)
	if not os.path.isdir(target_dir):
		os.makedirs(target_dir)
	if not os.path.isfile(target_file):
		print("unpacking to temporary dir", path)
		with open(target_file, "wb") as f:
			f.write(globals["vpk"][path].read())
	return target_file
	

def get_output_file(path):
	target_file = os.path.join("vpk/pak01_dir", path)
	target_dir = os.path.dirname(target_file)
	if not os.path.isdir(target_dir):
		os.makedirs(target_dir)
	return target_file


def get_header_bytes(header_file=None, file_size=-1, mp3=None):
	if header_file is None:
		header_file = globals["default_sound_header"]
	with open(get_path(header_file), "rb") as file:
		header = file.read()
		header_bytes = header[:header.index(b"\xff\xfb")]
		# mp3 sample count offset is 32 bytes from header end
		if mp3 is not None:
			duration = mp3.info.length
			sample_rate = mp3.info.sample_rate
			sample_count = int(duration * sample_rate)
			header_bytes = bytearray(header_bytes)
			header_bytes[-32:-28] = struct.pack("i", sample_count)
			header_bytes[-28:-24] = struct.pack("f", duration)
			if file_size >= 0:
				header_bytes[-12:-8] = struct.pack("i", file_size)
			#header_bytes = bytes(header_bytes)
			#print(header_bytes)
		return header_bytes
	

# main
	
remove_temp_dirs()

# setup global config
with open("overrides.json", "r") as overrides_file:
	config = json.loads(overrides_file.read())
	
set_vpk_path(get_vpk_dir())
	
if "default_sound_header" in config:
	globals["default_sound_header"] = config["default_sound_header"]

	
if "overrides" in config:
	for override in config["overrides"]:
		if "file" in override:		
			mp3_info = MP3(override["file"])
			with open(override["file"], "rb") as file:
				header_path = override["header_file"] if "header_file" in override else None
				file_data = file.read()
				if "apply" in override:
					for apply in override["apply"]:
						print("applying", override["file"], "to", apply)
						bytes = get_header_bytes(header_file=header_path, file_size=len(file_data), mp3=mp3_info) + file_data
						with open(get_output_file(apply), "wb") as out_file:
							out_file.write(bytes)
	
	print("assemble vpk")
	os.chdir("vpk")
	subprocess.run(["make_vpk.bat"])
	os.chdir("..")
	
	mods_dir = get_mods_dir()
	print("copy vpk to:", mods_dir)
	shutil.copyfile("vpk/pak01_dir.vpk", os.path.join(mods_dir, "pak01_dir.vpk"))
				
remove_temp_dirs()

					
