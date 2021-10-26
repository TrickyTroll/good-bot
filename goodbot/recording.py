from pathlib import Path
# Each recording module has to be imported here
from goodbot import editor, shell_commands, audio
from goodbot.utils import is_scene

def find_to_record():
    # TODO: Find each thing to record *in order*
    pass

def record_scene(scene_path: Path):
    # TODO: Record each command in a scene in order.
    pass

def record_project(project_path: Path):
    for potential_scene in project_path.iterdir():
        if is_scene(potential_scene):
            record_scene(potential_scene)
    pass

