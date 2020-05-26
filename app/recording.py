import subprocess
import pyautogui
import time

subprocess.Popen(["asciinema", "rec", "title2"])

pyautogui.write(" pip install numpy", interval=0.25)
pyautogui.press('enter')
time.sleep(5)

pyautogui.hotkey('ctrl', 'c')


