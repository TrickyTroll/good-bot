import time
import pyautogui
import subprocess

name = "a_cool_container"

subprocess.run(["docker", "build", "--tag", name, '.'])

subprocess.run([
    "docker", 
    "create", 
    "-it", 
    "--name", 
    'rocket-raccoon', 
    name])

subprocess.run([
    "docker",
    "start",
    "rocket-raccoon"])

print('Done!!!')
