# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml"]
# ///
"""The SessionStart hook: build and inject the initiative catalogue.

Fired on the three session beginnings that create a fresh context (startup,
clear, resume) and deliberately not on compaction, because the rebuild replaces
compaction rather than complementing it. The hook is code and holds no
judgement: it cannot converse with the developer and cannot invoke a skill, so
it only detects the fresh session and injects text. It reads the initiative
registry and each initiative's run-record directory, builds the initiative
catalogue (one entry per initiative: identifier, intent, status sentence, next
or last stage, recency), and prints the catalogue together with the
reconstitution protocol as additional context for the new session. The hook
injects no output artefact of any initiative: the prime skill performs every
artefact read after the developer confirms one initiative.

Registered in .claude/settings.json under hooks.SessionStart.
"""

from __future__ import annotations

import datetime
import re
import sys
from pathlib import Path

import yaml

RECONSTITUTION_PROTOCOL: str = """## Reconstitution protocol
1. If the initiative catalogue is empty, run the normal intake: ask what the
   developer needs, and classify the stated intent. None of the steps below
   applies.
2. If the focus note names one obvious continuation, open by proposing to
   resume that initiative, summarising its state from the catalogue entry above.
3. Otherwise present the catalogue and ask: continue an ongoing initiative,
   revisit a finished initiative, or start a new intent.
4. After the developer confirms one initiative, invoke the prime skill to read
   its run record and its output artefacts, state the rebuilt state, and
   continue at the next stage.
5. For a new intent, run the normal intake."""


def resolve_artefact_root(repo_root: Path) -> str:
    config_path: Path = repo_root / "sdlc.config.yaml"
    if config_path.exists():
        try:
            loaded: dict = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
            tree: dict = loaded.get("artefact_tree") or {}
            candidate = tree.get("root")
            if isinstance(candidate, str) and candidate:
                return candidate.rstrip("/")
        except yaml.YAMLError:
            pass
    return "ai_docs"


def initiative_recency(workspace: Path) -> str:
    """The most recent modification across the initiative workspace, ISO date."""
    latest: float = 0.0
    for path in workspace.rglob("*"):
        if path.is_file():
            modified: float = path.stat().st_mtime
            if modified > latest:
                latest = modified
    if latest == 0.0:
        return "never touched"
    stamp: str = datetime.date.fromtimestamp(latest).isoformat()
    return stamp


def main() -> int:
    repo_root: Path = Path.cwd()
    artefact_root: str = resolve_artefact_root(repo_root)
    registry_path: Path = repo_root / artefact_root / "initiatives" / "index.md"
    initiatives_dir: Path = registry_path.parent

    if not registry_path.exists():
        # No shared memory yet: inject nothing and let the normal intake run.
        return 0

    registry_text: str = registry_path.read_text(encoding="utf-8")

    lines: list[str] = ["# Session start: the initiatives on this project", ""]
    lines.append("## Initiative catalogue")

    entry_pattern: re.Pattern[str] = re.compile(r"^- \*\*(INIT-[^ *]+)", re.MULTILINE)
    entry_ids: list[str] = entry_pattern.findall(registry_text)

    catalogue_lines: list[str] = []
    for raw_line in registry_text.splitlines():
        stripped: str = raw_line.strip()
        if stripped.startswith("- **INIT-"):
            catalogue_lines.append(stripped)

    if not catalogue_lines:
        catalogue_lines.append("- (empty: the project has no initiative yet)")
    for entry_line in catalogue_lines:
        matched_id: re.Match[str] | None = re.search(r"INIT-[A-Za-z0-9-]+", entry_line)
        if matched_id is not None:
            workspace: Path = initiatives_dir / matched_id.group(0)
            if workspace.is_dir():
                recency: str = initiative_recency(workspace)
                lines.append(f"{entry_line} Last touched: {recency}.")
                continue
        lines.append(entry_line)

    focus_match: re.Match[str] | None = re.search(
        r"^The developer last confirmed (.+)$", registry_text, re.MULTILINE
    )
    if focus_match is not None and entry_ids:
        lines.append(f"- Focus note: the developer last confirmed {focus_match.group(1)}")

    lines.append("")
    lines.append(RECONSTITUTION_PROTOCOL)

    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
