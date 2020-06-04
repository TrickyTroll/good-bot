from functions import *
import time
from pathlib import Path

instructions_list = instruction_finder(Path('./'), Path('test.md'))

script_maker(instructions_list, Path('./'), Path('./'))

