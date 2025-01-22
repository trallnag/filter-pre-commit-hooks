# Develop!

This document is targeted at project developers. It helps people to make their
first steps. It also serves as a general entry to development documentation like
tooling configuration and usage.

Your environment should fulfill the following basic requirements:

- [Uv](https://docs.astral.sh/uv/) for managing Python-related things.
- [Pre-commit](https://pre-commit.com/). For managing and pre-commit Git hooks.
- [Task](https://taskfile.dev/). For running self-documenting tasks.
- Unix-like. Not required by itself, but assumed as the standard.

Common tasks like initialization and runnings tests are covered by and
documented in [`Taskfile.yaml`](Taskfile.yaml). To run a complete suite of
tasks, just invoke `task` without arguments.

This projects supports [Development Containers](https://containers.dev/). Check
out [`.devcontainer/README.md`](.devcontainer/README.md) for more information.
