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

subprocess.Popen([
    "docker",
    "attach",
    "rocket-raccoon"])

pyautogui.hotkeys('ctrl' 'l')
subprocess.run([
    "asciinema",
    "rec",
    file_name]) #file name still not defined.
# for every functions in the functions list:
    #run the function typing command

pyautogui.hotkey('ctrl', 'c') #This stops the asciinema recoding.

# The container should then be stopped.
time.sleep(5)
