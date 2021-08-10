# -*- coding: utf-8 -*-
"""
audio.py contains functions used by the cli module to record audio
contents using Google Cloud Text to Speech.
"""
from pathlib import Path
from rich.console import Console
from typing import List, Dict, Union, Any
from google.cloud import texttospeech


def fetch_audio_instructions(read_path: Path) -> List[Path]:
    """
    fetch_audio_instructions looks for files that can be used as audio
    instructions in the provided directory.

    Args:
        read_path (Path): A path towards the directory where this
        function will look for audio instructions files.
    Returns:
        List[Path]: A list of absolute paths towards each file that
        was found.
    """
    audio_recordings: List[Path] = []
    try:
        for rec in read_path.iterdir():
            if rec.suffix in ".txt" and "file_" in rec.name:
                audio_recordings.append(rec.resolve())
    except FileNotFoundError:
        return []

    return audio_recordings


def fetch_scene_audio_instructions(scene_path: Path) -> List[Path]:
    """
    fetch_scene_audio finds every audio instructions in
    a scene and returns it as a list.

    Args:
        scene_path (Path): The path towards the scene where this
        function will look for text to read.
    Returns:
        List[Path]: A list of paths towards each file that contains
        text to read in the provided scene.
    """
    scene_audio_instructions: List[Path] = []
    for directory in scene_path.iterdir():
        if str(directory.name).lower() == "read":
            scene_audio_instructions = scene_audio_instructions + fetch_audio_instructions(
                directory
            )
    return scene_audio_instructions


def fetch_project_audio_instructions(project_path: Union[Path, str]) -> List[Path]:
    """
    fetch_project_audio_instructions finds every audio instructions
    file in a Good Bot project.

    Args:
        project_path (Union[Path, str]): A path towards a Good Bot
        project.
    Returns:
        List[Path]: A list of absolute paths towards each audio
        instructions saved under the provided project path.
    """
    if not isinstance(project_path, Path):
        try:
            project_path = Path(project_path)
        except Exception as err:
            raise TypeError(f"Could not convert the provided argument to a Path object:\n{err}")
    all_audio_instructions: List[Path] = []
    for scene in project_path.iterdir():
        if "scene_" in scene.name:
            all_audio_instructions = all_audio_instructions + fetch_scene_audio_instructions(scene)
    return all_audio_instructions


def record_audio(
    project_path: Path, lang: str = "en-US", lang_name: str = "en-US-Standard-C"
) -> Path:
    """
    record_audio records audio by reading the `read` files using Google
    TTS.

    It records audio for a whole Good Bot project.

    Args:
        scene (click.Path): The path towards the files to read.
        Only the first line of these files will be read.
        save_path (click.Path): The path where the mp3 audio file
        will be saved. This does not include the file name, as it
        will be kept from the read path.
    Returns:
        click.Path: The path where the audio file is saved. This
        now includes the name of the file.
    """
    all_audio_scripts: List[Path] = fetch_project_audio_instructions(project_path)
    console: Console = Console()

    with console.status("[bold green]Recording audio...") as status:

        for script in all_audio_scripts:
            #
            save_path: Path = script.parent.parent / Path("audio")
            with open(script, "r") as stream:
                # Assuming everything to read is on one line
                to_read = " ".join(stream.readlines())

            client = texttospeech.TextToSpeechClient()

            synthesis_input = texttospeech.SynthesisInput(text=to_read)

            voice = texttospeech.VoiceSelectionParams(
                language_code=lang, name=lang_name, ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
            )

            audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

            response = client.synthesize_speech(
                input=synthesis_input, voice=voice, audio_config=audio_config
            )

            file_name = script.stem
            write_path = (save_path / file_name).with_suffix(".mp3")

            with open(write_path, "wb") as out:
                out.write(response.audio_content)
                console.log(f"Audio contents in file {script} has been recorded.")

    return save_path
