# Gist `filter_pre_commit_hooks.py`

Gist of a small Python script that extracts and filters
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

```re
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

```re
^ *(?:- )?id: [\'\"]?(?P<hook>[a-z0-9-]+)[\'\"]?.*#.*
[Tt]ags ?[:=] ?[0-9a-z, ]*\b(<tags>)\b[0-9a-z, ]*\..*$
```

## Versioning

The project follows [Semantic Versioning](https://semver.org/).

## Contributing

Contributions are welcome. Please refer to [`CONTRIBUTE.md`](CONTRIBUTE.md).

## Licensing

This work is licensed under the
[ISC License](https://en.wikipedia.org/wiki/ISC_license). See
[`LICENSE`](LICENSE) for the license text.

The license is also included in the script
[`src/filter_pre_commit_hooks.py`](src/filter_pre_commit_hooks.py) itself.
