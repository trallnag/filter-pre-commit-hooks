[![status](https://img.shields.io/badge/status-active-brightgreen)](#project-status)
[![release](https://img.shields.io/github/v/release/trallnag/filter-pre-commit-hooks)](https://github.com/trallnag/filter-pre-commit-hooks/releases)
[![ci](https://img.shields.io/github/actions/workflow/status/trallnag/filter-pre-commit-hooks/ci.yaml?label=ci)](https://github.com/trallnag/filter-pre-commit-hooks/actions/workflows/ci.yaml)
[![release](https://img.shields.io/github/actions/workflow/status/trallnag/filter-pre-commit-hooks/release.yaml?label=release)](https://github.com/trallnag/filter-pre-commit-hooks/actions/workflows/release.yaml)

# `filter_pre_commit_hooks.py`

Small Python script that extracts and filters
[pre-commit](https://pre-commit.com/) hooks so that only a subset can be run.
Why is such a script helpful? Pre-commit does not provide a way to run a
selection of hooks. It is only possible to skip hooks.

The standalone script is called `filter_pre_commit_hooks.py` and can be found
[here](src/filter_pre_commit_hooks.py). The license is included in the file.

It gets a comma-separated list of all pre-commit hooks except the ones specified
to be filtered out. The returned result can be used to set the `SKIP` env var to
only run a subset of hooks when executing a command like
`pre-commit run --all-files`.

Here it is used to run the hooks `foo` and `bar`:

```sh
export SKIP=$(python filter_pre_commit_hooks.py foo bar)
pre-commit run --all-files
```

The hook identifiers are extracted from the config using the following regex:

```text
^ *(?:- )?id: [\'\"]?(?P<hook>[a-z0-9-]+)[\'\"]?(?: +#.*)?$
```

Here it is used to run all hooks that are part of the `lint` group:

```sh
export SKIP=$(python filter_pre_commit_hooks.py --mode=group lint)
pre-commit run --all-files
```

In the latter case, the corresponding pre-commit config file looks like this:

```yaml
repos:
  - repo: local
    hooks:
      - id: ruff-format # Tags: format.
        language: system
        entry: I will not run
      - id: ruff-format # Tags: lint.
        language: system
        entry: I will run
```

The hook identifiers are extracted from the config using the following regex,
where `<tags>` is replaced by the given tags:

```text
^ *(?:- )?id: [\'\"]?(?P<hook>[a-z0-9-]+)[\'\"]?.*#.*
[Tt]ags ?[:=] ?[0-9a-z, ]*\b(<tags>)\b[0-9a-z, ]*\..*$
```

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
