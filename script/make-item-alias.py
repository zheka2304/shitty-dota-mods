import os
import os.path
import vpk
import shutil
import re
import json


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
	regex = "models.*crystal_maiden"#input("input regex to filter: ")
	regex = re.compile(regex)
	entries = search_vpk_entries(lambda x: re.search(regex, x))
	if len(entries) > 0:
		entries.sort(key=lambda x: x[1])
		for _, entry, _ in entries:
			print(entry)
		if True or yis_or_nah("create aliases for this files?"):
			origin = "crystal_maiden"#input("input origin to create aliases: ")
			item = "crystal_maiden_arcana"#input("input item to create aliases: ")
			all_candidates = list(map(lambda x: x[1], search_vpk_entries(lambda x: item in x)))
			result = []
			for _, entry, _ in entries:
				candidate_regex = entry[entry.rindex("/") + 1:]
				if origin in candidate_regex:
					candidate_regex = candidate_regex.replace(origin, ".*" + item + ".*")
					print(entry)
					candidate_regex = re.compile(candidate_regex)
					candidates = list(filter(lambda x: re.search(candidate_regex, x), all_candidates))
					print(candidates)
					if len(candidates) > 0:
						result.append([entry, candidates[0]])
			out_file_name = input("input result file name:")
			with open(out_file_name, "w") as out_file:
				out_file.write(json.dumps(result, indent=4))
	break
					
