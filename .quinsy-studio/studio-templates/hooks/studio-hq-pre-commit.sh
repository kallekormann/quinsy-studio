#!/bin/sh
# QUINSY-HQ-HOOK — commit the skilled studio, not the working notes.
# Installed by ./studio install. Additions only: a cleanup may still delete
# paths that were tracked before this rule.
toplevel=$(git rev-parse --show-toplevel) || exit 1
tmp=$(mktemp) || exit 1
trap 'rm -f "$tmp"' EXIT
git diff --cached --name-only --diff-filter=A > "$tmp" || exit 1
while IFS= read -r f; do
  [ -n "$f" ] || continue
  case "$f" in
    projects|projects/*)
      echo "quinsy HQ: refuse staging product path $f" >&2
      echo "Product git lives inside projects/<name>/ — never the studio index." >&2
      exit 1
      ;;
    intake|intake/*)
      echo "quinsy HQ: refuse staging intake path $f" >&2
      echo "Intake briefs stay on this machine." >&2
      exit 1
      ;;
    ideation|ideation/*)
      echo "quinsy HQ: refuse staging ideation notes $f" >&2
      echo "The ideation seed is .quinsy-studio/studio-templates/ideation/." >&2
      exit 1
      ;;
    .quinsy-studio/backlog|.quinsy-studio/backlog/*)
      echo "quinsy HQ: refuse staging backlog ticket $f" >&2
      echo "Infuse the lesson into knowledge-base/learnings/. The ticket stays local." >&2
      exit 1
      ;;
    .quinsy-studio/retros|.quinsy-studio/retros/*)
      echo "quinsy HQ: refuse staging retro $f" >&2
      echo "A retro stays local. The infused principle is what gets committed." >&2
      exit 1
      ;;
    .quinsy-studio/sprints|.quinsy-studio/sprints/*)
      echo "quinsy HQ: refuse staging studio sprint $f" >&2
      echo "Product sprints live in that product's own git repo." >&2
      exit 1
      ;;
    .quinsy-studio/knowledge-base/learnings/archive|.quinsy-studio/knowledge-base/learnings/archive/*)
      echo "quinsy HQ: refuse staging learning archive $f" >&2
      echo "The catalog in knowledge-base/learnings/ is the shared result." >&2
      exit 1
      ;;
    .quinsy-studio/knowledge-base/learnings/train-queue.json)
      echo "quinsy HQ: refuse staging the train queue $f" >&2
      echo "Closed train jobs stay local." >&2
      exit 1
      ;;
  esac
done < "$tmp"
