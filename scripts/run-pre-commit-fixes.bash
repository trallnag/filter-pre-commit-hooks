#!/usr/bin/env bash

set -euo pipefail

declare -x SKIP

SKIP=$(uv run --script scripts/filter_pre_commit_hooks.py fix task)

(pre-commit run --all-files || pre-commit run --all-files) \
  | grep --perl-regexp --invert-match --regexp='\.\e.+Skipped'
