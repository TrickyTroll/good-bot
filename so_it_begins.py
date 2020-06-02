import sys
from pathlib import Path
# According to the Dockerfile, everything is going to run in the directory /home/all
main_path = Path('/home/app')
# Since we don't want to record this directory, the main script is going to run 
# inside of a different one, called /tutorial.
working_path = Path('/tutorial')
# To access the user's video script, his or her $PWD will be mounted under /toto.
mount_path = Path('/toto')
import os
# To import from functions while being inside of /tutorial, we need to insert 
# a different path. functions.py is under /app.
sys.path.insert(1, main_path / 'app')
from functions import *

# This script is still running under /tutorial, and is fed a path towards a markdown file.
# This path is relative to /toto, since that's where the $PWD was binded.
filename = Path(sys.argv[1])

# Fetching the instructions inside script/script.md:
instructions_list = instruction_finder(mount_path, filename)

# Creating a new script and writing it inside of the new video folder.
new_script_path = new_script(instructions_list, script_path, main_path)

# Creating bash scripts for every item inside of the list:
shell_scripts_path = script_maker(instructions_list, main_path)

# Making an asciicast for every bash script:

asciicasts_path = instruction_executer(working_path, shell_scripts_path, main_path)


asciicast_transfer(asciicasts_path, mount_path)

script_transfer(new_script_path, mount_path)

cleanup()