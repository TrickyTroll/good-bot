# video-automation
Automating the recording of documentation videos using Video Puppet and Python!
## How it works
## Syntax

## Usage

1. Clone this repository.
2. Modify your_script.md respecting the syntax.
3. Build your container using ```docker build .```.
4. Run your container using ```docker run -it [container's id]```.
5. Fetch your video by running the `is_this_how_it_ends.py``` script.
6. Send the your_video folder to Video Puppet!

## What could be improved?

* The pathing is pretty bad. Should be done using pathlib instead of os.

* Giving users more options, like the colours of their terminal and the speed at which the 
typing is done.

* Making the value associated with "command" a list, allowing for multiple commands to be
recorded at the same time.

* A main script that builds the container, runs it, and transfers the data.

* Allowing more than just the gif format (stills and code formatted text cells could be 
useful.

* It's overall very syntax dependent, which is annoying.
