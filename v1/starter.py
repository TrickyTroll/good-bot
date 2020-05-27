import sys
sys.path.insert(1, './app')
from functions import *
sys.path.insert(1, './script')
name = 'helloWorld'

subprocess.Popen([
    'docker',
    'run',
    '--name',
    name,
    '--rm',
    '-it',
    'toto',
    'python3',
    'app.py'
    ])

instruction_executer(name, instruction_finder())



