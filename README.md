# good-bot

Automating the recording of documentation videos using Video Puppet and Python!

This cool application allows you to create terminal recordings using only a markdown file and 
a simple syntax.

## Usage

1. Clone this repository.

2. Write a markdown file that uses the syntax described below. You can see an example under 
the example folder.

3. Change your current working directory to this repo.

4. Build your container using ```docker build [--tag something you want] .```.

5. Change your current working directory to the one that contains your instruction file.

6. Run your container using ```docker run -it [--name something you want] -v $(PWD):/toto [the tag you chose] your_script.md ```.

7. Let the container do his thing. When it's done, a new folder called ```your_video``` should have been created
inside of your current working directory.

8. Send the content of the your_video folder to Video Puppet!

## How it works

To explain how good-bot works, let's first examine what it does.

![Where is x function running](https://docs.google.com/drawings/d/e/2PACX-1vSP3jd_BWWXzxL_WmsfMpxDAS5xrd2vLejp3PUAgnjejE_O5PDRzVk0lH8OzlZXcUZ6qVl_cfTcjxso/pub?w=960&h=720)

### The build

When the user builds a container using the Dockerfile, a container image is created. This 
image is based on Ubuntu and contains the directory in which the ```docker build``` command 
was executed. This is why you must build your container inside the main repository of this 
app.

The good-bot directory will be copied inside the container under the folder ```/home/all/```

The build will also create two other directories:

* ```/tutorial```: This is just a clean directory. It is where the commands specified in the 
instruction file are going to be executed.

* ```/usr/local/go/bin```: This is where ```ttyrec2gif``` can be called from.

### Running the container

####  Analyzing the docker run command

```docker run -it [--name something you want] -v $(PWD):/toto [the tag you chose] your_script.md ```

* ```-it```: This starts the container in interactive mode and gives it access to a pseudo-TTY. It's
required to allow the container to record itself.

* ```-v```: It bind mounts à volume. In this case, it binds the hosts ```$PWD``` to ```/toto``` inside
the container. ```$PWD``` can be replaced to whatever you want, but ```/toto``` should not be replaced.
Don't forget that ```your_script.md``` is actually a path relative to ```$PWD```. If you choose to change 
```$PWD```, you must change ```your_script.md``` accordingly. See the [documentation](https://docs.docker.com/storage/volumes/) to learn more.

* Naming your container isn't required, but it's a lot more easy to remember something cool like 
```rocker-raccoon``` compared to a long string of 12 letters and numbers.

#### What happends after you press enter

The last line of the ```Dockerfile``` is the container's [entrypoint](https://docs.docker.com/engine/reference/builder/#entrypoint).

```ENTRYPOINT ["python3", "/home/all/so_it_begins.py"]```

This tells docker that our container runs an executable in our case, everytime you run the container,
```so_it_begins.py``` will be executed using python3.

The python script also takes a path as an input. This path should guide the script towards your instruction 
file. It must be relative to ```$PWD```, or whatever you chose for the host's binding point.

Finally, ```so_it_begins.py``` also imports functions from ```app/functions.py``` that can do a 
few things:

1. ```instruction_finder```: Reads the file called ```your_script.md``` from 
the path provided as an argument to the python script. It looks under each ```hr``` if there is the string 
```(instructions:```. If the string is not present, it reads the next line, assuming that it 
is the file's header. In the case that the string  is there, instruction_finder creates 
a dictionary using the next 3 lines. The dictionary's format is 
```{"command": , "media_format": , "file_name"}```. The next 3 lines shoud then contain 
The commands to run, the media format (only gifs are supported for now), and the file name, 
respectively. Further details on the syntax can be found below. The dictionary is 
appended to a list, which is returned when the function has read through whole file.

2. ```new_script```: A new video script is created. This video plan respects 
[Video Puppet's](https://www.videopuppet.com/docs/format/) Markdown format. 
Whenever ```new_script``` is called, a new markdown file
is created by reading through the old one and removing the ```instructions``` mentions, 
replacing them with a line similar to: ```![freeze](somefile.gif)```.

3. ```script_maker```: This function creates a bash script for each instruction made by 
```instruction_finder```. The bash script imports ```demo-magic.sh``` and is made to follow 
[Demo-Magic's](https://github.com/paxtonhare/demo-magic) syntax. Demo-Magic is a bash script 
that automates typing of functions. This is useful because the commands will be typed 
and recorded inside the container without needing any input other that the initial 
markdown file from the user. The shell scripts are saved in a new folder called ```shell_scripts```.

4. ```instruction_executer```: Iters over every file inside of ```shell_scripts``` and 
runs the scripts while recoding using [Ttyrec](https://nethackwiki.com/wiki/Ttyrec). Ttyrec 
creates data files that will allow you to replay what happened on your terminal while Ttyrec 
was recoding. These files can later be converted into gifs.

5. ```ttyrec_transfer```: The name is a bit missleading. Not only does it transfers your recordings to a 
new folder, but it also converts them into gifs using [Ttyrec2gif](https://github.com/sugyan/ttyrec2gif). 
The new folder is created under ```/toto```, which is binded to the host. This means that this folder will 
be accessible even after the container has completed his run.

6. ```script_transfer```: A bit less missleading. This just copies the script created by ```new_script``` 
to the same folder where the gifs were saved. This folder is called ```your_video```. 
This folder is what you can send to Video Puppet to create a video!


All the previous steps ran inside the Ubuntu docker container. This allows you to run 
commands that install stuff that you already have locally an still go through the 
installation steps. It also allows you install whatever you want without having to remove it 
from your computer afterwards!

#### For the visual type of people

![what is x function doing](https://docs.google.com/drawings/d/e/2PACX-1vSL3QEHcWukD-dDqg4ml-wIuV_KK_kfjEA20drzrVLy_69L2QEt_znLHFbHITivdTqZHQhQKQBBfDHd/pub?w=960&h=720)


## Syntax

Here is an example of the very pointillous syntax that you ~~sould~~ must use:

```
---
size: 1080p
---
(instructions:
	[command]
	[media_format]
	[file_name]
)

```

### Recommendations

* Adding ```asset-resize: contain``` to your header. This tells Video Puppet not to scale your gifs.

* Adding ```background: corporate-1``` to your header. This soundtrack is staight fire.

## What could be improved?

* ~~The pathing is pretty bad. Should be done using pathlib instead of os.~~

* Giving users more options, like the colours of their terminal and the speed at which the 
typing is done.

* Making the value associated with "command" a list, allowing for multiple commands to be
recorded at the same time.

* ~~A main script that builds the container, runs it, and transfers the data.~~

* Allowing more than just the gif format (stills and code formatted text cells could be 
useful).

* ~~It's overall very syntax dependent, which is annoying.~~

* The recording quality. It's bad.
