import subprocess
import time
import pyautogui

subprocess.Popen([
    'docker',
    'run',
    '-it',
    'toto',
    'asciinema',
    'rec'
    ])
time.sleep(3)
pyautogui.write('echo hello world', interval = .25)
pyautogui.press('enter')
time.sleep(20)
#pyautogui.write('exit')
#pyautogui.press('enter')
#subprocess.Popen(['asciinema', 'rec', '-c', "python3 commander.py", 'name'])
