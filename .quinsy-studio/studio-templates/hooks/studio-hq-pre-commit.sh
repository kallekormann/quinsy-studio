#!/bin/sh
# QUINSY-HQ-HOOK — studio root must not stage projects/
# Installed by ./studio install (LO-0317). Product git lives in projects/<name>/.
toplevel=$(git rev-parse --show-toplevel) || exit 1
tmp=$(mktemp) || exit 1
trap 'rm -f "$tmp"' EXIT
git diff --cached --name-only > "$tmp" || exit 1
while IFS= read -r f; do
  [ -n "$f" ] || continue
  case "$f" in
    projects|projects/*)
      echo "quinsy HQ: refuse staging product path $f" >&2
      echo "Product git lives inside projects/<name>/ — never the studio index." >&2
      exit 1
      ;;
  esac
done < "$tmp"
