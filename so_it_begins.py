import sys
from pathlib import Path
# According to the Dockerfile, everything is going to run in the directory /home/all
main_path = Path('/home/all')
# Since we don't want to record this directory, the main script is going to run 
# inside of a different one, called /tutorial.
working_path = Path('/tutorial')
# To access the user's video script, his or her $PWD will be mounted under /toto.
mount_path = Path('/toto')

import os
# To import from functions while being inside of /tutorial, we need to insert 
# a different path. functions.py is under /app.
sys.path.insert(1, str(main_path / 'app'))

from functions import *

# IMPORTANT: Most functions return paths created using pathlib. Variables are used to
# store these paths so that they can be used later in the script.

# This script is still running under /tutorial, and is fed a path towards a markdown file.
# This path is relative to /toto, since that's where the $PWD was binded.
filename = Path(sys.argv[1])

# Fetching the instructions inside script/script.md:
instructions_list = instruction_finder(mount_path, filename)

# Creating a new script and writing it inside of the new video folder.
# Reads from mount_path and writes in main_path.
new_script_path = new_script(instructions_list, mount_path, main_path, filename)

# Creating bash scripts for every item inside of the list:
# Reads from instructions_list and writes in main_path.
shell_scripts_path = script_maker(instructions_list, main_path, main_path / 'app')

# Making an asciicast for every bash script:
# Reads from she shell_scrips directory and writes in the main path.
ttyrecs_path = instruction_executer(working_path, shell_scripts_path, main_path)

# Reads from the directory that contains the recordings.
# Writes in the mounted volume.
ttyrec_transfer(ttyrecs_path, mount_path)

# Reads from the directory that contains the new script.
# Writes in the mounted volume.
script_transfer(new_script_path, mount_path)

# This function does nothing..for now.
cleanup()