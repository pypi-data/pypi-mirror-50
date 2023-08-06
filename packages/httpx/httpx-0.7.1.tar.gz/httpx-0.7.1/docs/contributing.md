# Contributing

Thank you for being interested in contributing with HTTPX.
There are many ways you can contribute with the project:

- Try HTTPX and [report bugs/issues you find](https://github.com/encode/httpx/issues/new)
- [Implement new features](https://github.com/encode/httpx/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22)
- [Review Pull Requests of others](https://github.com/encode/httpx/pulls)
- Write documentation
- Participate in discussions

## Reporting Bugs or Other Issues

Found something that HTTPX should support?
Stumbled upon some unexpected behavior?

Feel free to open an issue at the
[issue tracker](https://github.com/encode/httpx/issues).
Try to be more descriptive as you can and in case of a bug report,
provide as much information as possible like:

- OS platform
- Python version
- Installed dependencies and versions (`python -m pip freeze`)
- Code snippet
- Error traceback

## Development

To start developing HTTPX create a **fork** of the
[HTTPX repository](https://github.com/encode/httpx) on GitHub.

Then clone your fork with the following command replacing `YOUR-USERNAME` with
your GitHub username:

```shell
$ git clone https://github.com/YOUR-USERNAME/httpx
```

With the repository cloned you can access its folder, set up the
virtual environment, install the project requirements,
and then install HTTPX on edit mode:

```shell
$ cd httpx
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r test-requirements.txt
$ pip install -e .
```

!!! note
    Feel free to replace this step with your development environment setup
    (pyenv, pipenv, virtualenvwrapper, docker, etc).

## Testing and Linting

We use [nox](https://nox.thea.codes/en/stable/) to automate testing, linting,
and documentation building workflow. Make sure you have it installed
at your system before starting.

Install nox with:

```shell
$ python3 -m pip install --user nox
```

Alternatively, use [pipx](https://github.com/pipxproject/pipx) if you prefer
to keep it into an isolated environment:

```shell
$ pipx install nox
```

Now, with nox installed run the complete pipeline with:

```shell
$ nox
```

!!! warning
    The test suite spawns a testing server at the port **8000**.
    Make sure this isn't being used, so the tests can run properly.

To run the code auto-formatting separately:

```shell
$ nox -s lint
```

Also, if you need to run the tests only:

```shell
$ nox -s test
```

You can also run a single test script like this:

```shell
$ nox -s test -- tests/test_multipart.py
```

## Documenting

To work with the documentation, make sure you have `mkdocs` and
`mkdocs-material` installed on your environment:

```shell
$ pip install mkdocs mkdocs-material
```

To spawn the docs server run:

```shell
$ mkdocs serve
```
