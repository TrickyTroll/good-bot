# `good-bot` 🤖

Automating the recording of documentation videos.

`good-bot` automates the process of recording documentation for your
projects. It even provides voice-over using
[Google TTS](https://cloud.google.com/text-to-speech/).

## Quickstart

> How to quickly get started with `good-bot`.

The easiest way to install `good-bot` is to pull the Docker
[image](https://hub.docker.com/r/trickytroll/good-bot). The
image has every tool required by the program pre-installed.
The only requirement is that you have a working 
[Docker](https://www.docker.com) installation.

Once you have pulled the image, you can try good bot using
the following command.

```shell
docker run -it trickytroll/good-bot:latest
```

> **Note:** You can also just run the previous command and
> the image will be pulled automatically.

Every `good-bot` command also requires a configuration file.
Since those files reside on your computer, you will need to
pass them to the container so that the program can read
them.

Passing file to a container is quite simple using 
[`volumes`](https://docs.docker.com/storage/volumes/). In short
you will need to add the following flag and argument to the
previous `docker run` command.

```shell
--volume $PWD:/project
```

The complete command looks like this:

```shell
docker run -it --volume $PWD:/project trickytroll/good-bot:latest
```

This will bind your current working directory to the container's
`/project` directory.

You can now use `good-bot`'s command line interface to record
a video.

If you are not feeling like writing a script for now but still
want to see what `good-bot` is capable of, you can use the
[no audio](./examples/basics/no-audio.yaml) example.

> For more detailed instructions on unlocking all of `good-bot`'s
> capabilities, si the full installation [instructions](#install).

## Install

> Installing the most recent version of `good-bot` locally and
> with Docker.

### Local install

#### ⚠️ Warnings
>
> 1. `good-bot` has quite a few dependencies.
>    Installing locally is not the most straightforward way
>    of using this program.
>
> 2. By following your instructions, this program might
>    install new software on your computer. It might also
>    edit text files and modify you system.
>    Using this program in a container ensures that your
>    environment is not affected by your demos. It also
>    lets you install programs many times in a row for your
>    demos without having to uninstall them between each
>    recording session.

#### Dependencies

The Docker image is built on the Ubuntu linux distribution, which
uses the `apt` package manager and a specific repository to fetch
it's packages.

The following program can be installed on `Ubuntu` using `apt`, but
they are probably distributed for your package manager too. If they
are not, please see each program's website for more in depth
installation instructions.

| Dependency | Version |
| ---------- | ------- |
| `python`   | `3.9`   |
| `asciinema`| `2.0.3` |
| `pip`      | `20.0.2`|

Python dependencies are specified in the
[`requirements.txt`](./requirements.txt) file.

These dependencies are only the ones required for `good-bot` to work.
Your own scripts might requires other programs to work. It is up to
you to install those other missing parts.

#### Install locally

`good-bot` should be installed using `pip`. From the root of this
project, run the following command. Also make sure that you are
installing from branch `main`. The `latest` branch contains more
recent changes, but there is no guarantee that the program will
work if installed from `latest`.

```shell
pip install .
```

This will install `runner` in your current Python environment.

### Docker install

#### Using `docker build`

`good-bot` is a containerized application. To use the app, you must have
a working [Docker](https://www.docker.com) installation.

To build the container, simply run `docker build -t [SOME TAG] .` in the
same directory as the `Dockerfile`. `[SOME TAG]` is to be replaced by
a name of your choosing.

#### Pull the image

The image is built on the `main` branch on every changes. The following
command will pull the `good-bot` container image.

```shell
docker pull trickytroll/good-bot:latest
```

## Usage

> Instructions on how to use `good-bot`, whether it is installed locally
> or in a Docker container.


### Docker usage

#### Creating a project with the Docker image

Once you have written your configuration file, you can create your project
using `good-bot`'s `setup` command.

```bash
docker run -it -v $PWD:/project -t [SOME TAG] setup [CONFIG NAME]
```

Where

- `[SOME TAG]` is the tag previously chosen.
- `[CONFIG NAME]` is the name of the configuration file.

> Keep in mind that this command mounts the current working directory
> in the container. If your configuration file is not under your
> current working directory, the previous command won't work.

#### Recording your video in a container

If you have a project directory, you can record your clips using

```bash
docker run -it -v $PWD:/project -t [SOME TAG] record [PROJECT NAME]
```

Where

- `[SOME TAG]` is the tag previously chosen.
- `[PROJECT NAME]` is the name of the project file.

> **Note**: This is where you need to include the `--env`
> and `-v` flags mentionned [earlier](#adding-voice-over).

### Local usage

If installed locally, this program's command line interface can be
used with the `good-bot` command.

#### Setting up

### Adding voice-over

If you want to use `Google TTS`, you will need an API key for the service.
To get your code, you can follow the [instructions](https://cloud.google.com/text-to-speech/docs/quickstart-protocol)
provided by Google.

Once you have activated the API, you'll be able to download a `.json` file that
contains your key. As mentionned in the Google TTS documentation, you will also
need to bind the path to your `.json` file to the `GOOGLE_APPLICATION_CREDENTIALS`
variable.

When `goodbot` runs, it will look for the value of the
`GOOGLE_APPLICATION_CREDENTIALS` environment variable. Instructions on setting
this variable depend on the installation method.

#### TTS on your local machine

Once you have downloaded the API key file, the last step is to set the
`GOOGLE_APPLICATION_CREDENTIALS` environment variable to the path
towards the location of the key on your computer. On UNIX-like systems
this can be done using the following command.

```shell
export GOOGLE_APPLICATION_CREDENTIALS=[path/to/file.json]
```

where `[path/to/file.json]` must be replaced by the path to your own
credentials file.

#### TTS with the Docker image

This is where instructions differ from the ones in Google's documentation.
Since your host's
environment variables are not sent to the container by default, you will
need to pass the `.json` credentials file to the container. The environment
variable needs to be set for the container, not just the host.

To copy your private key to the container, you can add the following flag
when running the container:

```shell
-v [PATH/TO/FILE]:/.env
```

Where `[PATH/TO/FILE]` needs to be replaced by the path towards the directory
that contains your key on your host's filesystem. This mounts the previously
mentionned directory in your container under the path `/.env`.

Now that your API key is accessible from container, you can set the
`GOOGLE_APPLICATION_CREDENTIALS` variable using the following command:

```bash
--env GOOGLE_APPLICATION_CREDENTIALS="/.env/[KEY-NAME].json
```

Where `KEY-NAME` needs to be replaced by the name of the `.json` file
previously downloaded.

#### Voice-over summary

To use voice-over, you will need to activate the Google Text to Speech
API for your Google Cloud account. You will also need an API key, which
can be downloaded as a `.json` file.

Once you have your key on your host computer, you can share the key to
the container and enable it by adding the following flags to the `docker run`
command (see [Recording your video](#recording-your-video)).

```bash
-v [PATH/TO/FILE]:/.env --env GOOGLE_APPLICATION_CREDENTIALS="/.env/[KEY-NAME].json
```

`[PATH/TO/FILE]` and `[KEY-NAME]` must be replaced by your own values.

## For the old version

To see the first release, please go to the
[old](https://github.com/TrickyTroll/good-bot/tree/old) branch.
