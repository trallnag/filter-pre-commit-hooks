# Release!

This document is targeted at project maintainers. It describes the process to
release a new version.

## Preparation

Pick a name for the new release. It must follow
[Semantic Versioning](https://semver.org):

```sh
VERSION=1.0.1
```

Make sure that the "Unreleased" section in the [changelog](CHANGELOG.md) is
up-to-date. Feel free to adjust entries for example by adding additional
examples or highlighting breaking changes.

Move the content of the "Unreleased" section that will be included in the new
release to a new section with an appropriate title for the release. Should the
"Unreleased" section now be empty, add "Nothing." to it.

## Trigger

Commit the changes. Make sure to sign the commit:

```sh
git add CHANGELOG.md
git commit -S -m "chore: Prepare release v$VERSION"
git log --show-signature -1
```

Push changes:

```sh
git push origin master
```

Check
[workflow runs](https://github.com/trallnag/filter-pre-commit-hooks/actions?query=branch%3Amaster)
in GitHub Actions and ensure everything is fine.

Tag the latest commit with an annotated and signed tag:

```sh
git tag -s v$VERSION -m ""
git show v$VERSION
```

Make sure that the tree looks good:

```sh
git log --graph --oneline --all -n 5
```

Push the tag itself:

```sh
git push origin v$VERSION
```

This triggers the release workflow which will build binaries, build and push
container images, and draft a GitHub release. Monitor the
[release workflow run](https://github.com/trallnag/filter-pre-commit-hooks/actions/workflows/release.yaml).

## Wrap Up

Go to the release page of this project on GitHub
[here](https://github.com/trallnag/filter-pre-commit-hooks/releases) and review
the automatically created release draft.

Publish the draft.
