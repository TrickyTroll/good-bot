# This file contains functions used by other scripts
import shlex
import time
import sys
import os
#import pyautogui
import subprocess

def instruction_finder():
    '''
    This function searches for funtions to be executed inside
    of the container.
    The video's script name must be 'script.md'.
    Returns: A list of functions to be executed.
    Function's structure:
    {command: , media_format: , file_name: }
    '''
    todo = []
    with open('script/script.md') as f:
        datafile = [line for line in f.readlines() if line.strip()]

        # Here the program should also skip the header.
        for line in datafile:
            index = datafile.index(line)
            if '---' in line and '(instructions:' in datafile[index+1]:
                to_add = {
                        "command": datafile[index+2].rstrip().lstrip(),
                        "media_format": datafile[index+3].rstrip().lstrip(),
                        "file_name": datafile[index+4].rstrip().lstrip()
                        }
                todo.append(to_add)

            elif '---' in line and '(instructions:' not in datafile[index+1]:

                print("Line %s has no instructions")%(datafile[index+1])
                
                break

    return todo


# ----------------------------------------------------------------------- #
#                             Recording
# ----------------------------------------------------------------------- #

def start_rec(instructions):
    '''
    Starts asciinema and sets the name of the
    recording to the file_name variable.
    Returns: Should be recording.
    '''
    title = instructions["file_name"]
    subprocess.Popen([
        'asciinema',
        'rec',
        title])
    
    return 'Sould be recording'


def stop_rec():
    '''
    Stops asciinema using 'ctrl + d'
    '''
    subprocess.run(['exit'])
    return 'Sould have stopped'


# ----------------------------------------------------------------------- #
#                         Instrucion executer
# ----------------------------------------------------------------------- #

def run_command(instructions):
    '''
    Input: some text to type in the
    terminal. Must be of type string
    Returns: The string 'Done!'.
    '''
    command = instructions["command"]

    start_rec(instructions)

    os.system('clear')
    time.sleep(.5)

    subprocess.Popen(shlex.split(command)) 

    stop_rec()

    return 'Done!'



def instruction_executer(container_name, instructions_list):
    '''
    Writes functions in a terminal using 
    pyautogui.

    Input: A list of instructions to execute.
    The format of each instruction is a dict
    containing: the command, the media format 
    and the file name.

    Returns: A string saying 'Done!'.
    '''
    for i in instructions_list:
        if i["media_format"] == 'gif':
            run_command(i)

    return 'Done!'
        

