from functions import instruction_executer

instructions = {
        "command": 'echo hello world',
        "media_type": 'static',
        "file_name": 'test'
        }
hello = [instructions]

instruction_executer(hello)
