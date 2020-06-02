# This file contains functions used by other scripts
import shutil
from pathlib import Path
import shlex
import time
import stat
import sys
import os
import subprocess

# ----------------------------------------------------------------------- #
#                    Finding the instructions
# ----------------------------------------------------------------------- #

def instruction_finder(path_to_script):
    '''
    path_to_script: The path towards the video script that you wrote.

    Returns: A list of functions to be executed.
    Function's structure:
    {command: , media_format: , file_name: }
    '''
    todo = []
    with open('script/your_script.md', "r") as f:
        datafile = [line for line in f.readlines() if line.strip()]
        index = 0
        for line in datafile:
            # The '(instructions:' part allows the program to skip headers.
            if '---' in line and '(instructions:' in datafile[index+1]:
                to_add = {
                        "command": datafile[index+2].rstrip().lstrip(),
                        "media_format": datafile[index+3].rstrip().lstrip(),
                        "file_name": datafile[index+4].rstrip().lstrip()
                        }
                todo.append(to_add)

            index += 1

    return todo

# ----------------------------------------------------------------------- #
#                        Editing the script 
# ----------------------------------------------------------------------- #
def new_script(instructions_list):
    '''
    Takes the instructions_list from instruction_finder(). Uses the 
    instructions to generate a new script file, formatted to work using 
    Video Puppet.

    Input: A list of instructions. Instructions are dictionnaries created 
    with the instruction_finder() function.

    Returns: 'New file created!'
    '''

    print(os.getcwd())
    with open('../script/your_script.md', 'r') as f:
        lines = f.readlines()
    with open('../script/script.md', 'w') as f:
        index = 0
        title_index = 0

        while index < len(lines):
            
            # current_line_edited could be replaced by changing the 
            # next 'if' statement by if '---' in current_line.
            current_line_edited = lines[index].rstrip().lstrip()
            current_line = lines[index]

            if current_line_edited != "---":
                f.write(current_line)
                index += 1
            
            elif current_line_edited == "---":
                # This statement skips the header.
                if index == 0:
                    f.write(current_line)
                    index += 1
                else:
                    current_title = instructions_list[title_index]["file_name"]
                    media_format = instructions_list[title_index]["media_format"]
                    f.write(current_line)
                    f.write("![freeze](%s.%s)\n"%(current_title, media_format))
                    index += 6
                    title_index += 1 

    return 'New file created!'

# ----------------------------------------------------------------------- #
#                       Bash scripts creation
# ----------------------------------------------------------------------- #

def script_maker(instructions_list):
    '''
    Creates a bash script that uses demo-magic for every instruction in the
    list.
    Input: List of instructions that is generated by instruction_finder()
    Returns: 'Done!'
    '''
    # Making a new directory for the scripts.

    parent = os.getcwd()
    newpath = parent + "/app/shell_scripts"
    
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    # Changing to the new working directory.

    os.chdir(newpath)

    # Creating the scripts.
    
    for i in instructions_list:
        identification = '%s.sh'%(i['file_name'])
        with open (identification, 'w') as shscr:
            shscr.write('''\
#!/usr/bin/env bash

# including demo-magic

. ./demo-magic.sh

# speed (defined by the user)

TYPE_SPEED=%s
                    
# This should also be defined by the user...maybe later.

DEMO_PROMPT="${GREEN}➜ ${CYAN}\W "

# Clearing the prompt

clear

# The commands go here

pe "%s"

# The end (shows a prompt at the end)

p ""
'''%(10, i['command']))#Commands should be a list at some point
            
            # Making sure that the files are executable

        os.chmod(identification, stat.S_IRWXU)



    return 'Done!'

# ----------------------------------------------------------------------- #
#                             Recording
# ----------------------------------------------------------------------- #


def start_rec(to_record):
    '''
    Creates a new directory and saves the video inside of the 
    directory.
    Records to_record using asciinema.
    to_record: shoud be a shell script created by script_maker.
    Returns: 'Sould be recording...'
    '''
    # Defines the title of the video to the shell script's name
    # and the path to the new directory.
    
    title = './recordings' + '/' + to_record.replace('.sh', '')

    # Starting asciinema

    subprocess.run([
        'asciinema',
        'rec',
        '--overwrite',
        '-q',
        '-c',
        './shell_scripts/' + to_record,
        title
        ])
    return 'Should be recording...'
    


# ----------------------------------------------------------------------- #
#                         Instrucion executer
# ----------------------------------------------------------------------- #

def instruction_executer(path_to_scripts):
    '''
    loops through every scripts inside to the folder provided by
    path_to_scripts. Runs the function start_rec for each script.

    The path is relative to the app folder.

    Returns 'Everything has been executed!'
    '''

    # Creating the new directory

    os.chdir('..')

    newpath = os.getcwd()+ "/recordings"
    print(newpath)
    
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    # Executing start_rec for each.

    for filename in os.listdir(path_to_scripts):

        start_rec(filename)

    return 'Everything has been executed!' 


# ----------------------------------------------------------------------- #
#                         Asciicast converting
# ----------------------------------------------------------------------- #
# This function is not in use.
def asciicast_2gif(path_to_asciicasts, path_to_save):
    '''
    path_to_asciicasts: the path of the folder where the asciicasts
    are saved.
    
    path_to_save: the path of the folder where the gifs are going to
    be saved.

    Converts the asciicasts in path_to_asciicasts
    into gifs, and saves them inside of path_to_save.

    Returns 'Done!'
    '''

    for filename in os.listdir(path_to_asciicasts):

        subprocess.run([
           'asciicast2gif',
           './recordings/' + str(filename),
           path_to_save / (str(filename) + '.gif')
            ])

    return 'Done!'

# ----------------------------------------------------------------------- #
#                               Conversion
# ----------------------------------------------------------------------- #


def asciicast_transfer():
    '''
    This function Creates a new directory for the end product. 
    It then converts asciicasts to gifs and saves the gifs in the 
    your_video directory using asciicast_2gif.
    '''

    current = Path('.')
    newpath = current / "your_video"
    
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    asciicast_2gif('./recordings', newpath)
        
    return 'Done'

def script_transfer():
    '''
    Transfers the script created to the your_video folder.
    '''
    
    subprocess.run([
        'cp',
        '/home/tutorial/script/script.md',
        './your_video'
        ])
    return 'Done!'

def cleanup():
    '''
    This functions cleans up the directory so that it can be used for another
    video!
    '''
    return None
