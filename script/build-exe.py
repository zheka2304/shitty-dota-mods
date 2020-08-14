import os
import os.path
import shutil
import subprocess
import sys
import zipfile


def zipdir(path, zip_file):
	ziph = zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED)
	for root, dirs, files in os.walk(path):
		for file in files:
			ziph.write(os.path.join(root, file))			
	ziph.close()


def execute(cmd, message=None, error_message="Failed", ok_message="OK"):
	if message is None:
		message = "running " + cmd[0]	
	print(message + "...")
	sys.stdout.flush()
	try:
		subprocess.run(cmd, stdout=sys.stdout)
		print("..." + ok_message)
	except Exception as e:
		print(error_message, "with", e)

os.chdir("virtual-env/Scripts")
execute(["activate.bat"])

# pyinstaller creates directories dist, build, and file app.spec in current directory
# result exe location: dist/app.exe
execute(["./pyinstaller.exe", "--onefile", "../../script/app.py"], "installing requirements...")

print("SUCCESS, copying files...")


BUILD_DIR = "shitty-dota-mods"

if os.path.isdir("../../build/" + BUILD_DIR):
	shutil.rmtree("../../build/" + BUILD_DIR)
os.makedirs("../../build/" + BUILD_DIR)
shutil.copyfile("dist/app.exe", "../../build/" + BUILD_DIR + "/app.exe")
shutil.rmtree("dist")
shutil.rmtree("build")
os.remove("app.spec")

# back to root
os.chdir("../..")

if os.path.isdir("vpk/pak01_dir"):
	shutil.rmtree("vpk/pak01_dir")
if os.path.isfile("vpk/pak01_dir.vpk"):
	os.remove("vpk/pak01_dir.vpk")
shutil.copytree("vpk", "build/" + BUILD_DIR + "/vpk")

print("creating zip...")
os.chdir("build")
if os.path.isfile(BUILD_DIR + ".zip"):
	os.path.remove(BUILD_DIR + ".zip")
zipdir(BUILD_DIR, BUILD_DIR + ".zip")
os.chdir("..")

print("\nDONE!")