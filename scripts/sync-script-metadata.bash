#!/usr/bin/env bash

#
# This script synchronizes the required Python version, dependencies, and
# dependency versions from the project config to the script inline metadata.
#

set -euo pipefail

# Extract metadata from config.
metadata=$(
  sed --quiet '7,12p' pyproject.toml \
    | sed 's/^/# /' \
    | sed 's/[[:space:]]\+$//'
)

# Remove current metadata from script.
stripped_script=$(sed '21,26d' src/filter_pre_commit_hooks.py)

# Insert new metadata into script.
{
  echo "$stripped_script" | head -n 20
  echo "$metadata"
  echo "$stripped_script" | tail -n +21
} > src/filter_pre_commit_hooks.py
