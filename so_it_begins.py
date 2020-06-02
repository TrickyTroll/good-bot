import sys
from pathlib import Path
sys.path.insert(1, '/home/app/app')
from functions import *

filename = Path(sys.argv[1])
print(filename)
# Fetching the instructions inside script/script.md:
instructions_list = instruction_finder(filename)

# Creating bash scripts for every item inside of the list:
script_maker(instructions_list)

# Making an asciicast for every bash script:

instruction_executer('./shell_scripts')

# Creating a new script and writing it inside of the new video folder.

new_script(instructions_list)

asciicast_transfer()

script_transfer()

cleanup()