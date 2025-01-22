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

import subprocess
import sys
from argparse import ArgumentParser
from dataclasses import dataclass

VERSION = "1.0.1"

ANSI_RED = "\033[31m"
ANSI_GREEN = "\033[32m"
ANSI_BLUE = "\033[34m"
ANSI_RESET = "\033[0m"


@dataclass
class CmdExecErrorInfo:
    """Information about a command execution error."""

    cmd_index: int
    cmd_short: str
    exit_code: int


parser = ArgumentParser(
    description=(
        "Executes given commands and defers errors until all commands have "
        "been executed. Once all commands have been executed, a short summary "
        "is printed."
    ),
    epilog=(
        "For more information, check out "
        "<https://github.com/trallnag/exec-cmds-defer-errors>."
    ),
)

parser.add_argument(
    "-v",
    "--version",
    action="version",
    version=f"%(prog)s {VERSION}",
)

parser.add_argument(
    "commands",
    nargs="+",
    help=("Commands to execute. Every command is executed in its own shell."),
)


if __name__ == "__main__":
    args = parser.parse_args()

    commands: list[str] = args.commands

    if not all(commands):
        parser.error("All given commands must be non-empty strings.")

    cmd_exec_errors: list[CmdExecErrorInfo] = []

    for index, command in enumerate(commands):
        print(f"{ANSI_BLUE}Executing command {index + 1}{ANSI_RESET}...")
        print(f"{ANSI_BLUE}{command.strip()}{ANSI_RESET}")

        # Rule S602 disabled as running arbitrary code in shell is intended here.
        completed_process = subprocess.run(command, shell=True, check=False)  # noqa: S602
        if completed_process.returncode == 0:
            print(
                f"{ANSI_GREEN}Executed command {index + 1} "
                f"successfully.{ANSI_RESET}"
            )
        else:
            print(
                f"{ANSI_RED}Executed command {index + 1} "
                f"failed with exit code {completed_process.returncode}.{ANSI_RESET}"
            )

            cut_off_limit = 30
            cmd_short = (
                f"{command[:cut_off_limit]}..."
                if len(command) > cut_off_limit
                else command
            )

            cmd_short = cmd_short.replace("\r\n", " ").replace("\n", " ")

            cmd_exec_errors.append(
                CmdExecErrorInfo(
                    cmd_index=index + 1,
                    cmd_short=cmd_short,
                    exit_code=completed_process.returncode,
                )
            )

    if not cmd_exec_errors:
        print(
            f"{ANSI_GREEN}All {len(commands)} commands "
            f"executed successfully.{ANSI_RESET}"
        )

        sys.exit(0)
    else:
        print(
            f"{ANSI_RED}{len(cmd_exec_errors)} out of "
            f"{len(commands)} command(s) failed.{ANSI_RESET}"
        )

        for cmd_exec_error in cmd_exec_errors:
            print(
                f"{ANSI_RED}Command {cmd_exec_error.cmd_index} "
                f"failed with exit code {cmd_exec_error.exit_code}: "
                f"{cmd_exec_error.cmd_short}{ANSI_RESET}"
            )

        sys.exit(1)
