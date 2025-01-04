#
# /// script
# requires-python = ">=3.10"
# ///
#
# This work is available under the ISC license.
#
# Copyright Tim Schwenke <tim@trallnag.com>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED “AS IS” AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
# LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
# OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.
#

import re
from argparse import ArgumentParser, BooleanOptionalAction
from pathlib import Path
from typing import Literal

VERSION = "1.1.0"

parser = ArgumentParser(
    description=(
        "Gets a comma-separated list of all pre-commit hooks except the ones "
        "specified to be filtered out. The returned result can be used to set "
        "the `SKIP` env var to only run a subset of hooks when executing a "
        "command like `pre-commit run --all-files`."
    ),
    epilog=(
        "For more information, check out "
        "<https://github.com/trallnag/filter-pre-commit-hooks>."
    ),
)

parser.add_argument(
    "-v",
    "--version",
    action="version",
    version=f"%(prog)s {VERSION}",
)

parser.add_argument(
    "--config",
    type=Path,
    default=".pre-commit-config.yaml",
    help=("Path to the pre-commit config. Defaults to `%(default)s`."),
)

parser.add_argument(
    "--fail-unknown",
    action=BooleanOptionalAction,
    default=True,
    help=(
        "Fail if an unknown hook is specified to be filtered out. "
        "Only relevant in the case of `id` mode. Defaults to `%(default)s`."
    ),
)

parser.add_argument(
    "--mode",
    choices=["id", "tag"],
    default="id",
    help=(
        "Mode to use when filtering out hooks. `id` looks for the hook id "
        "declared as an ordinary attribute. `tag` looks for the hook tag. "
        "Defaults to `%(default)s`."
    ),
)

parser.add_argument(
    "filters",
    type=str,
    nargs="+",
    help=(
        "What to filter out, i.e. what should not show up in the resulting "
        "list. In the `id` mode, these are the hook identifiers themselves to "
        "exclude. In the `tag` mode, these are the hook identifiers that are "
        "associated with at least one of the specified tags to exclude."
    ),
)

if __name__ == "__main__":
    args = parser.parse_args()

    config: Path = args.config
    fail_unknown: bool = args.fail_unknown
    mode: Literal["id", "tag"] = args.mode
    filters: list[str] = args.filters

    with open(args.config) as pre_commit_config:
        pre_commit_config_content: str = pre_commit_config.read()

    # All hook identifiers that have been found in the pre-commit config file.
    all_hooks: set[str] = set(
        match.group("hook")
        for match in re.compile(
            r"^ *(?:- )?id: [\'\"]?(?P<hook>[a-z0-9-]+)[\'\"]?(?: +#.*)?$",
            re.MULTILINE,
        ).finditer(pre_commit_config_content)
    )

    # All hook identifiers that should not be part of the final result set.
    excluded_hooks: set[str]

    if args.mode == "id":
        # Excluded hooks are the ones that have been specified as filters.
        excluded_hooks = set(args.filters)

        if args.fail_unknown:
            unknown_hooks = excluded_hooks - all_hooks

            if len(unknown_hooks) > 0:
                parser.error(f"Unknown hook(s): {sorted(list(unknown_hooks))}")
    else:
        # Validate that all filters are valid tags.
        regex = re.compile(r"^[a-z0-9]+$")
        for filter in args.filters:
            if not regex.match(filter):
                parser.error(
                    (
                        f"Invalid filter value: '{filter}'. "
                        f"Must match regex: '{regex.pattern}'."
                    )
                )

        # Excluded hooks are determined based on tags given as filters.
        excluded_hooks = set(
            match.group("hook")
            for match in re.compile(
                (
                    r"^ *(?:- )?id: [\'\"]?(?P<hook>[a-z0-9-]+)[\'\"]?.*#.*"
                    r"[Tt]ags ?[:=] ?[0-9a-z, ]*\b(<tags>)\b[0-9a-z, ]*\..*$"
                ).replace("<tags>", "|".join(args.filters)),
                re.MULTILINE,
            ).finditer(pre_commit_config_content)
        )

    filtered_hooks = all_hooks - excluded_hooks

    print(",".join(sorted(list(filtered_hooks))))
