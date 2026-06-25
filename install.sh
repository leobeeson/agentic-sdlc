#!/usr/bin/env bash
# Bootstrap the agentic SDLC framework into a target repository.
#
# Usage: ./install.sh /path/to/target-repo
#
# Copies this repository's .claude directory into the target repository root.
# After running, open Claude Code in the target repository (restart the session
# if it was already open) and run the setup skill.

set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 /path/to/target-repo" >&2
  exit 1
fi

TARGET="$1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE="$SCRIPT_DIR/.claude"

if [ ! -d "$TARGET" ]; then
  echo "Error: target directory does not exist: $TARGET" >&2
  exit 1
fi

if [ ! -d "$SOURCE" ]; then
  echo "Error: framework .claude not found at: $SOURCE" >&2
  exit 1
fi

mkdir -p "$TARGET/.claude"
cp -R "$SOURCE/." "$TARGET/.claude/"

echo "Agentic SDLC framework copied into: $TARGET/.claude"
echo
echo "Next steps:"
echo "  1. Open Claude Code in $TARGET (restart the session if it was already open)."
echo "  2. Run the setup skill (/setup) to create the artifact tree and sdlc.config.yaml."
echo "  3. Drive the pipeline phase by phase: initialise-project, define-requirements,"
echo "     design-architecture, plan-implementation, then implement-task for each task."
