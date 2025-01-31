#!/bin/bash

declare -x SKIP

SKIP=$(uv run scripts/filter_pre_commit_hooks.py --mode=tag lint)

pre-commit run --all-files \
  | grep --perl-regexp --invert-match --regexp='\.\e.+Skipped'
