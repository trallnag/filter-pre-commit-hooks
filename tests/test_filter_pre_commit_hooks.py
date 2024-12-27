import subprocess


def run_with(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            "uv",
            "run",
            "src/filter_pre_commit_hooks.py",
            *args,
        ],
        capture_output=True,
        shell=False,
        check=False,
        text=True,
    )


def test_unknown_fail_default() -> None:
    """
    Tests that the script by default fails when an unknown hook is specified to
    be excluded.
    """

    result = run_with("prettier", "foo", "bar")
    assert result.returncode != 0
    assert "Unknown hook(s): ['bar', 'foo']" in result.stderr


def test_unknown_fail_explicit() -> None:
    """
    Tests that the script fails when an unknown hook is specified to be excluded
    and this behavior is configured explicitly.
    """

    result = run_with("--fail-unknown", "prettier", "foo", "bar")
    assert result.returncode != 0
    assert "Unknown hook(s): ['bar', 'foo']" in result.stderr


def test_unknown_pass_explicit() -> None:
    """
    Tests that the script does not fail when an unknown hook is specified to be
    excluded and this behavior is configured explicitly.
    """

    result = run_with("--no-fail-unknown", "prettier", "foo", "bar")
    assert result.returncode == 0


def test_filter_out_hooks_by_id() -> None:
    """
    Tests that the script successfully filters out hooks by their id.
    """

    result = run_with("prettier", "destroyed-symlinks", "yamlfmt", "ruff-fix")
    assert result.returncode == 0
    assert result.stdout.strip().split(",") == [
        "check-added-large-files",
        "check-case-conflict",
        "check-executables-have-shebangs",
        "check-merge-conflict",
        "check-shebang-scripts-are-executable",
        "check-vcs-permalinks",
        "check-yaml",
        "detect-aws-credentials",
        "detect-private-key",
        "end-of-file-fixer",
        "fix-byte-order-marker",
        "forbid-new-submodules",
        "mixed-line-ending",
        "mypy",
        "ruff-format",
        "ruff-lint",
        "trailing-whitespace",
    ]


def test_filter_out_hooks_by_tag() -> None:
    """
    Tests that the script successfully filters out hooks by tags.
    """

    result = run_with("--mode=tag", "lint", "whatever")
    assert result.returncode == 0
    assert result.stdout.strip().split(",") == [
        "end-of-file-fixer",
        "fix-byte-order-marker",
        "mixed-line-ending",
        "mypy",
        "prettier",
        "ruff-fix",
        "ruff-format",
        "ruff-lint",
        "trailing-whitespace",
        "yamlfmt",
    ]
