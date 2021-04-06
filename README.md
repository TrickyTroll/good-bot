# `good-bot` 🤖

Automating the recording of documentation videos.

`good-bot` automates the process of recording documentation for your
projects. It even provides voice-over using 
[Google TTS](https://cloud.google.com/text-to-speech/).

## Try it out

If you want to try good-bot for yourself, you can use the provided
[example](https://github.com/TrickyTroll/good-bot/blob/main/examples/goodbot.yaml).

### Building the container

`good-bot` is a containerized application. To use the app, you must have
a working [Docker](https://www.docker.com) installation.

To build the container, simply run `docker build -t [SOME TAG] .` in the
same directory as the `Dockerfile`. `[SOME TAG]` is to be replaced by
a name of your choosing.

### Adding voice-over

If you want to use `Google TTS`, you will need an API key for the service.
For now, `good-bot` looks for your key in a `.env` directory. The file
must be named `google-tts.json`.

### Creating a project

Once you have written your configuration file, you can create your project
using `good-bot`'s `setup` command.

```bash
docker run -it -v $(PWD):/project -t [SOME TAG] setup [CONFIG NAME]
```

Where

* `[SOME TAG]` is the tag previously chosen.
* `[CONFIG NAME]` is the name of the configuration file.

> Keep in mind that this command mounts the current working directory
> in the container. If your configuration file is not under your
> current working directory, the previous command won't work.

### Recording your video

If you have a project directory, you can record your clips using

```bash
docker run -it -v $(PWD):/project -t [SOME TAG] record [PROJECT NAME]
```

Where

* `[SOME TAG]` is the tag previously chosen.
* `[PROJECT NAME]` is the name of the project file.

## For the old version

To see the first release, please go to the
[old](https://github.com/TrickyTroll/good-bot/tree/old) branch.