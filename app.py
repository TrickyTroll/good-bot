# import docker
#client = docker.from_env()

#print(client.containers.run("ubuntu", "echo 'hello world'"))

import subprocess

subprocess.run(["xterm", "-hold", "-e", "python3 /home/tricky/Documents/video_automation/recording.py"])


#screen_rec()
#pyautogui.write(" echo 'Hello world!' ", interval=0.25)
#pyautogui.press('enter')
