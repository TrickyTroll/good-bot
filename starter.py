# This function should be used if the docker is already created and running.
import sys
import time
import subprocess
sys.path.insert(1, './app')
from functions import *
sys.path.insert(1, './script')

subprocess.Popen([
    'docker',
    'attach',
    'rocket-raccoon'])

time.sleep(1)

instruction_executer(instruction_finder())



