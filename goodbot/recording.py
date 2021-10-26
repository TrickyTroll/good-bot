from goodbot.utils import is_scene

def record_project(project_path: Path):
    for potential_scene in project_path.iterdir():
        if is_scene(potential_scene):
            record_scene(potential_scene)
    pass

