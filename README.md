[![status](https://img.shields.io/badge/status-active-brightgreen)](#project-status)
[![release](https://img.shields.io/github/v/release/trallnag/filter-pre-commit-hooks)](https://github.com/trallnag/filter-pre-commit-hooks/releases)
[![ci](https://img.shields.io/github/actions/workflow/status/trallnag/filter-pre-commit-hooks/ci.yaml?label=ci)](https://github.com/trallnag/filter-pre-commit-hooks/actions/workflows/ci.yaml)
[![release](https://img.shields.io/github/actions/workflow/status/trallnag/filter-pre-commit-hooks/release.yaml?label=release)](https://github.com/trallnag/filter-pre-commit-hooks/actions/workflows/release.yaml)

# `filter_pre_commit_hooks.py`

Small Python script that extracts and filters
[pre-commit](https://pre-commit.com/) hooks so that only a subset can be run by
pre-commit. Why is such a script helpful? Pre-commit only provides a way to skip
hooks. There is no way to explicitly state which hooks should be run.

The standalone script is called `filter_pre_commit_hooks.py` and can be found
[here](src/filter_pre_commit_hooks.py). The license is included in the file.

By default, the script returns all hooks that are tagged as required. In the
following example, it is used to run all hooks that are tagged with `fix` and
`task`:

```sh
SKIP=$(uv run filter_pre_commit_hooks.py fix task) pre-commit run -a
```

Note that in the example the script is executed with `uv run`. A subcommand of
[uv](https://docs.astral.sh/) a package manager for Python. This is because the
script contains
[inline script metadata](https://packaging.python.org/en/latest/specifications/inline-script-metadata/#inline-script-metadata)
specifying required dependencies.

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
[`.pre-commit-config.yaml`](.pre-commit-config.yaml). Some tasks in
[`Taskfile.yaml`](Taskfile.yaml) run selected pre-commit hooks using the script.

## Project status

The project is maintained by me, [trallnag](https://github.com/trallnag), and I
am interested in keeping it alive as I am actively using it.

## Versioning

The project follows [Semantic Versioning](https://semver.org/).

## Contributing

Contributions are welcome. Please refer to [`CONTRIBUTE.md`](CONTRIBUTE.md).

## Licensing

This work is licensed under the
[ISC license](https://en.wikipedia.org/wiki/ISC_license). See
[`LICENSE`](LICENSE) for the license text.

The license is also included in the script
[`src/filter_pre_commit_hooks.py`](src/filter_pre_commit_hooks.py) itself.

## Template

This project is based on the following
[Copier](https://copier.readthedocs.io/en/stable/) template:
<https://github.com/trallnag/copier-template-python-script>.
