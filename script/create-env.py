import os
import os.path
import shutil
import subprocess
import sys


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


os.chdir("..")
if os.path.isdir("virtual-env"):
	print("removing old virtual environment...")
	shutil.rmtree("virtual-env")

execute(["python", "-m", "venv", "virtual-env"], message="creating virtual environment")

os.chdir("virtual-env/Scripts")
execute(["activate.bat"])
execute(["pip3.exe" if os.path.isfile("pip3.exe") else "pip.exe", "install", "-r", "../../script/requirements.txt"], "installing requirements...")
os.chdir("../..")

print("\nDONE!")