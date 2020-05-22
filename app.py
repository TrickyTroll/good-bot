# import docker
#client = docker.from_env()

#print(client.containers.run("ubuntu", "echo 'hello world'"))

import subprocess
import pyautogui

subprocess.call(['gnome-terminal'])

# start recording

# start typing

pyautogui.write(" echo 'Hello world!' ", interval=0.25)
pyautogui.press('enter')
