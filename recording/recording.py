# Records a terminal window

# Allows to convert the screenshots as numpy arrays.
import numpy as np
# To create the video
import opencv-python
# To take the screenshots.
import pyautogui
# To call our bash script and find window coordinates.
import subprocess

# Finding the screen's size using term_finder
subprocess.call("bash term_finder.sh")

# Defining the codec and creating the output object.
fourcc = cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter("output.avi", fourcc, 30.0, (SCREEN_SIZE))


