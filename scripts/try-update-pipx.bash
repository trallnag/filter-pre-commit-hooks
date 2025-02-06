#!/bin/bash

set -euo pipefail

if command -v pipx &> /dev/null; then
  installed=$(pipx list -q --short)

  for pkg in "$@"; do
    if echo "$installed" | grep -q "^$pkg .*$"; then
      pipx upgrade -q "$pkg"
    fi
  done
fi
