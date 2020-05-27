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
    'bash'
    ])

instruction_executer(name, instruction_finder())



