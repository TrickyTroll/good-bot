import sys
sys.path.insert(1, './app')
from functions import *
# Using the your_video directory
containers_name = input('The name of the container: ')
# Initiating Docker (for asciicast2gif):
transfer_init()
# Transferring asciicasts to your_video and converting:
asciicast_transfer(containers_name)

# Transferring the new scripts
script_transfer(containers_name)

cleanup()
