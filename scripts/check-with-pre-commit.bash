#!/bin/bash

set -euo pipefail

declare -x SKIP

SKIP=$(uv run --no-config scripts/filter_pre_commit_hooks.py check task)

pre-commit run --all-files \
  | grep --perl-regexp --invert-match --regexp='\.\e.+Skipped'
