# Reproducing examples

## Examples from [`basics`](./basics)

Since those examples only require a simple `good-bot` installation,
you can follow the instructions from the main [`README`](../README.md).

## Examples from [`passwords`](./passwords)

Those examples require two containers to test an `ssh` connection. To
simplify this task, a `docker-compose.yml` file is
[provided](./passwords/docker-compose.yml). From the passwords examples
[directory](./passwords), run the following command.

```shell
docker-compose run good-bot
```
