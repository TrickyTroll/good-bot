import os
import sys
import yaml
import click
import shutil
import subprocess

from pathlib import Path
########################################################################
#                               YAML parsing                           #
########################################################################


def config_parser(file: click.File) -> dict:
    """Can be used to parse a configuration file.

    Args:
        file (click.File): The configuration file. This should be
        handled by click.

    Returns:
        dict: A dict with the parsed information.
    """
    parsed_file = yaml.safe_load(file)
    
    if type(parsed_file) != dict:
        click.echo("Your config is not formatted properly.")
        click.echo(parsed_file)
        sys.exit()

    return parsed_file


def config_info(parsed_config: dict) -> dict:
    """
    Returns useful info on the configuration file.

    Args:
        parsed_config (dict): The parsed configuration file. This should
        be handled by the config_parser func.

    Returns:
        dict: A dictionary that contains usful information about the
        configuration.
    """

    all_confs = {}

    CONF_TEMPLATE = {
        "commands": [],
        "expect": [],
        "scenes": [],
        "editor": [],
        "slides": [],
        "read": []
    }

    for keys, values in parsed_config.items():
        
        if not values:

            click.echo(f"Scene #{keys} is empty, please remove it.")
            sys.exit()

        conf_info = CONF_TEMPLATE.copy()

        for item in values:
            for k, v in item.items():
                if k == "commands":
                    to_append = {}
                    to_append["command"] = item["commands"]
                    if "expect" in item.keys():
                        to_append["expect"] = item["expect"]
                    conf_info["commands"].append(to_append)
                elif k == "expect":
                    continue
                elif k == "read":
                    conf_info["read"].append(v)
                elif k == "slides":
                    conf_info["slides"].append(v)
                elif k == "editor":
                    conf_info["editor"].append(v)
                else:
                    click.echo(f'"{k}" is not a supported command.')
                    sys.exit()
        
        all_confs[keys] = conf_info

    return all_confs

########################################################################
#                       Creating directories                           #
########################################################################

def create_dirs_list(all_confs: dict) -> Path:

    dirs_list = []

    for k, v in all_confs.items():

        to_create = []

        for keys, values in v.items():
            if values: # There are items in the list.
                to_create.append(keys)
            

        if "read" in to_create:
            to_create.append("audio") # MP3 files

        # Those dirs are created no matter the content
        to_create.append("gifs") # Gifs files
        to_create.append("recording") # MP4 files
        to_create.append("project") # Final video

        dirs_list.append({f"scene_{k}": to_create})

    return dirs_list

def create_dirs(directories: list, project_dir: str = "my_project") -> Path:
    """Creates directories for the project. This function should be
    called on the host's computer, not in the container. Docker will
    mount the project afterwards.

    Args:
        directories (list): A list of subdirs to create
        project_dir (str, optional): The name of the project. It will
        be used to name the root directory for the project.
         Defaults to "my_project".

    Returns:
        Path : The path towards where the project has been created if
        the command succeded. If it didn't, this returns the path
        towards the current directory.
    """
    project_dir = Path(project_dir)
    overwrite = False

    if project_dir.is_dir():

        click.echo(f"Directory {project_dir} exists!")
        resp = input(f"Would you like to overwrite {project_dir}?: ")

        if resp.lower() == "yes":

            # Erase the directory
            overwrite = True
            confirm = input(f"Are you sure you want to remove {project_dir}?: ")
            shutil.rmtree(project_dir)

            # Then make a new one

            os.mkdir(project_dir)

        else:
            sys.exit()

    else:
        os.mkdir(project_dir)

    for item in directories:

        # There should only be one key, no need for
        # a for loop.
        scene_id = list(item.keys())[0]
        scene = Path(scene_id)

        # There should only be one value too
        # This shoud probably stored as a tuple now that
        # I think about it...
        for directory in list(item.values())[0]:

            new_dir = project_dir / scene / Path(directory)

            if new_dir.is_dir() and not overwrite:
                click.echo(f"Folder {new_dir} exists!")
            else:
                os.makedirs(new_dir)

    return project_dir.absolute()

def split_config(parsed: click.File, project_path: Path) -> Path:
    """Splits the main config file into sub configurations for
    every type of action.

    Args:
        parsed (click.File): The parsed configuration file. This
        should be handled by the `parse_config` function.
        project_path (Path): The path towards the project. This
        path is returned by the `create_dirs` function.

    Returns:
        Path: The same project path that was passed.
    """
    todos = config_info(parsed)

    # This should probably be grouped
    for k, v in todos.items():

        scene_path = Path(f"scene_{k}")

        for key, value in v.items():

            write_path = Path(key)

            if "read" in key:
                ext = ".txt" 
            else:
                ext = ".yaml"

            for i in range(len(value)):

                try:
                    to_write = yaml.safe_dump(value[i])
                
                except TypeError:
                    sys.exit()
                
                file_name = Path(f"file_{i}")
                file_path = (project_path / scene_path / write_path / file_name)

                click.echo(f"Creating {file_path.with_suffix(ext)}")
                
                with open(file_path.with_suffix(ext), "w") as file:
                    
                    file.write(to_write)
        
    return project_path


########################################################################
#                             Video creation                           #
########################################################################


def is_scene(directory: Path) -> bool:
    """Checks if a directory is a scene that contains instructions.
    
    Args:
        directory (pathlib.Path): The path towards the directory to 
        check.
    Returns:
        bool: Wether the directory is a scene that contains elements
        or not.
    """
    to_return = False
    dir_name = directory.name
    contains_something = any(directory.iterdir())
    
    if dir_name[0:5] == "scene" and contains_something:
        
        to_return = True
    
    return to_return
    
def list_scenes(project_dir: click.Path) -> Path:
    """Lists scenes in the project directory.
    
    Args:
        project_dir (click.Path): The path towards the location of the
        project.
    Returns:
        list: A list of directories (Paths).
    """
    project_dir = Path(project_dir)
    to_return = []
            
    return [thing for thing in project_dir.iterdir() if is_scene(thing)]

def record_commands(scene: Path) -> Path:
    """Records a gif for every video in the commands directory of the
    specified scene.
    
    Args:
        scene (pathlib.Path): The path towards the scene to record.
    Returns:
        pathlib.Path: The path towards the gif that has been recorded.
        If nothing has been recorded, this function returns the path
        of the current working directory instead.
    """
    is_commands = Path("commands") in [item for item in scene.iterdir()]
    
    if not is_commands:
        return Path(os.getcwd())
    else:
        commands_path = scene / Path("commands")
        
    for command in commands_path.iterdir():
        subprocess.run([
            "asciinema",
            "rec",
            "-c",
            "runner",
            
        ])
    pass