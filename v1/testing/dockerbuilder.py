import docker
import pyautogui

client = docker.from_env()

client.images.build(path = '.', tag = 'a_cool_container')
x = client.containers.create(image = 'a_cool_container')

x.start(tty = True)
x.exec_run('echo hello world', tty=True)

