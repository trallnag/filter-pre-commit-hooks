#!/usr/bin/env bash

#
# This script runs pre-commit hooks that are tagged with "check" and "task".
#

set -euo pipefail

declare -x SKIP

SKIP=$(./scripts/filter_pre_commit_hooks.py check task)

pre-commit run --all-files \
  | grep --perl-regexp --invert-match --regexp='\.\e.+Skipped'
