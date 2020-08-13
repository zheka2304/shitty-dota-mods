import os
import os.path
import vpk
import shutil
import re


def get_dota_dir():
	with open("dota-dir.txt", "r") as file:
		return file.read();


dota_dir = get_dota_dir();
vpks = [];
for file in os.listdir(dota_dir):
	if file[-4:] == ".vpk":
		vpks.append(os.path.join(dota_dir, file));

def search_vpk_entries(check):
	result = []
	for vpk_file in vpks:
		try:
			vpk_interface = vpk.VPK(vpk_file);
			for vpk_entry in vpk_interface:
				if check(vpk_entry):
					result.append((vpk_interface, vpk_entry, vpk_file));
		except ValueError:
			pass
	return result;

	
def yis_or_nah(message, default=False):
	result = input(message + " [" + ("Y/n" if default else "N/y") + "]:").lower()
	return result == "y" if result in ("y", "n") else default

'''
offset = 0
with open("test\\sounds\\music\\valve_dota_001\\music\\killed.vsnd_c", "rb") as f:
	original = f.read();
	offset = original.index(b"\xff\xfb")

print(offset, "\n"*5)
with open("the_world.mp3", "rb") as f:
	the_world = f.read();
	
with open("the_world.vsnd_c", "wb") as f:
	f.write(original[:offset] + the_world)
'''


while True:
	command = input("input command or regex expression to search: ")
	pattern = re.compile(command)
	entries = search_vpk_entries(lambda x: re.match(pattern, x))
	if len(entries) > 0:
		entries.sort(key=lambda x: x[1])
		for _, entry, _ in entries:
			print(entry)
		if yis_or_nah(str(len(entries)) + " matched found, extract?"):
			output_dir = input("enter output dir: ");
			for vpk_interface, vpk_entry, _ in entries:
				out_path = os.path.join(output_dir, vpk_entry)
				out_dir = os.path.dirname(out_path)
				if not os.path.isdir(out_dir):
					os.makedirs(out_dir)
				with open(out_path, "wb") as file:
					file.write(vpk_interface[vpk_entry].read());
					
