# Contribution guidelines

## Installing developpement dependencies

### Using `flit`

`good-bot` is packaged using
[`flit`](https://flit.readthedocs.io/en/latest/index.html).
This is also the program to use if you want to install the
developpement dependencies.

To install `flit` in your current environment, you can use
`pip`.

```shell
pip install flit
```

Once `flit` is installed, installing dependencies can be done
by running the following command from the root of this project.

```shell
flit install
```

## Testing

### How?

To run tests, you should use `pytest` from the root of this project.

```shell
pytest .
```

For the tests to work properly, you will need to install `good-bot`'s
dependencies to your current environment.

To do so, you can use `pip` to install the dependencies specified in
the `requirements.txt` file. From the root of the project:

```shell
pip install -r requirements.txt
```

If you are having problems installing the dependencies on your
system, see [Using `docker-compose`](#using-docker-compose).

You will also need to install `pytest`. This can be done using the
following command.

```shell
pip install pytest
```

### Tools

`good-bot` is tested using a mix of `pytest` and `unittest`. Feel free
to write your tests in any of those two tools. As long as your test
functions start with `test_`, `pytest` will take them into account.

### Where to write tests

Tests are written in the [`tests`](./tests) directory. Each file in the
[`goodbot`](./goodbot) directory has its own test file.

This means that if you add functions to the file
[`funcmodule.py`](./goodbot/funcmodule.py), you should test those
functions in the file [`test_funcs.py`](./tests/test_funcs.py).

If you extend `good-bot` by creating a new module, please create a
separate test file for your module.

### Using `docker-compose`

If some programs used by `good-bot` are difficult to install on your
system, you can also use Docker to run tests.

The [`docker-compose`](./docker-compose.yml) file specifies two
different test services:

* `test`: This simply runs pytest on `good-bot`'s source code with
  no flag and no arguments.
* `test-cov`: This service runs `pytest` with the `--cov` flag to
  also get a coverage report for the testing suite.

To use any of those services, simply run

```shell
docker-compose run test
```

or

```shell
docker-compose run test-cov
```

from the root of this project.

## Style guidelines

`good-bot` is styled using [`black`](https://github.com/psf/black).

Once you are ready to push your code, simply run black on the whole project.

```shell
black .
```

The style guidelines are defined in the
[`pyproject.toml`](./pyproject.toml) file under the
`tool.black` section.
