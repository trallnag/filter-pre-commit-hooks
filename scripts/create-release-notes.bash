#!/usr/bin/env bash

set -euo pipefail

mkdir -p tmp

release_notes=tmp/release-notes.md

awk '/^## /{count++} count==2{print} count==3{exit}' CHANGELOG.md \
  | tail +2 \
  | awk 'NF {p=1} p' | tac \
  | awk 'NF {p=1} p' | tac \
  | sed 's/^### /## /' \
    > $release_notes

mdformat --wrap=no $release_notes
