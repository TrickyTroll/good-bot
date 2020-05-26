import keyboard
import subprocess
import time

keyboard.press_and_release('ctrl+l')

subprocess.Popen(['asciinema', 'rec', 'title'])

keyboard.write('echo hello world')
keyboard.press_and_release('enter')

keyboard.press_and_release('ctrl+d')
