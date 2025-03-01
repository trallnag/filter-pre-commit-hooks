[![status](https://img.shields.io/badge/status-active-brightgreen)](#project-status)
[![release](https://img.shields.io/github/v/release/trallnag/filter-pre-commit-hooks)](https://github.com/trallnag/filter-pre-commit-hooks/releases)
[![ci](https://img.shields.io/github/actions/workflow/status/trallnag/filter-pre-commit-hooks/ci.yaml?label=ci)](https://github.com/trallnag/filter-pre-commit-hooks/actions/workflows/ci.yaml)
[![release](https://img.shields.io/github/actions/workflow/status/trallnag/filter-pre-commit-hooks/release.yaml?label=release)](https://github.com/trallnag/filter-pre-commit-hooks/actions/workflows/release.yaml)

# Filter-pre-commit-hooks

Small Python program that extracts and filters
[pre-commit](https://pre-commit.com/) hooks so that only a subset of them can be
executed. Why is such a program helpful? Pre-commit only provides a way to skip
hooks. There is no way to explicitly state which hooks should be run.

The program is available in this repository as the script
[`filter_pre_commit_hooks.py`](./src/filter_pre_commit_hooks/filter_pre_commit_hooks.py)
and as the package
[filter-pre-commit-hooks](https://pypi.org/project/filter-pre-commit-hooks/) on
PyPI.

By default, the program returns all hooks that have the given tags. In the
following example, all pre-commit hooks that are tagged with `fix` and `task`
are executed (tagging is described further below):

```sh
SKIP=$(uv run -s filter_pre_commit_hooks.py fix task) pre-commit run -a
```

The program itself is executed with `uv run`, a subcommand of
[uv](https://docs.astral.sh/), which is a package manager for Python. This is
because the script contains
[inline script metadata](https://packaging.python.org/en/latest/specifications/inline-script-metadata/#inline-script-metadata)
specifying required dependencies. The script also contains a shebang, so it can
be executed directly.

Using the package from PyPI, the equivalent command looks like this:

```sh
SKIP=$(filter-pre-commit-hooks fix task) pre-commit run -a
```

Tags are extracted from the "alias" field of every hook. Tags are declared by
putting them into parenthesis at the end of the respective alias. Individual
tags are separated by commas. Here are two exemplary aliases:

```txt
forbid-new-submodules (check, task)
mixed-line-ending (fix, task)
```

Options can be passed to the script to change the behavior of the script. For
example, to filter hooks by their identifier instead of their tags. For more
information on this, try out the `--help` option of the script or read the
source code.

A valid config used with the script can be found in
[`.pre-commit-config.yaml`](./.pre-commit-config.yaml). Some tasks in
[`Justfile`](./Justfile) run selected pre-commit hooks using the script.

## Shell completion

This program uses [Click](https://click.palletsprojects.com/en/stable/) for the
CLI. Click provides automatically generated shell completion for Bash, Fish, and
Zsh. Check out the official documentation
[here](https://click.palletsprojects.com/en/stable/shell-completion/).

## Project status

The project is maintained by me, [Tim](https://github.com/trallnag), and I am
interested in keeping it alive as I am actively using it.

I'm also using the project to test out various tools and workflows.

## Versioning

The project follows [Semantic Versioning](https://semver.org/).

## Contributing

Contributions are welcome. Please refer to [`CONTRIBUTE.md`](./CONTRIBUTE.md).

## Licensing

This work is licensed under the
[ISC license](https://en.wikipedia.org/wiki/ISC_license). See
[`LICENSE`](./LICENSE) for the license text.

The license is also included in the script
[`filter_pre_commit_hooks.py`](./src/filter_pre_commit_hooks/filter_pre_commit_hooks.py)
itself.

## Template

This project is based on the following
[Copier](https://copier.readthedocs.io/en/stable/) template:
<https://github.com/trallnag/copier-template-python-script>.
