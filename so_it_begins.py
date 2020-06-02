import sys
sys.path.insert(1, './app')
from functions import *

filename = str(sys.argv)[0]
# Fetching the instructions inside script/script.md:
instructions_list = instruction_finder('./script/your_script.md')

# Creating bash scripts for every item inside of the list:
script_maker(instructions_list)

# Making an asciicast for every bash script:

instruction_executer('./shell_scripts')

# Creating a new script and writing it inside of the new video folder.

new_script(instructions_list)

asciicast_transfer()

script_transfer()

cleanup()