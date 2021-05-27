# -*- coding: utf-8 -*-
"""`goodbot` program.

`goodbot` is a program that generates video documentation automatically
from a script. No terminal recording is required on your part. You don't
even need to record audio! `goodbot` uses Google TTS to generate `mp3`
files from your scripts.

## Code

See the `funcmodule` for most of the code. From file parsing to audio
content recording, it's all in the `funcmodule.py` file.

## Example

If you have everything installed on your computer, you can record a
video by using the `setup` and `record` commands.

```shell
goodbot setup [path/to/script]
```

Where `[path/to/script]` is the path towards your `.yaml` configuration
file.

```shell
goodbot record [path/to/dir]
```

Where `[path/to/dir]` is the path towards the directory created by the
setup command.

See the documentation on Github (github.com/TrickyTroll/good-bot) for
more information.
"""

__version__ = "0.1.0"
