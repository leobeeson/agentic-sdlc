# /// script
# requires-python = ">=3.11"
# dependencies = ["pydantic>=2", "pyyaml"]
# ///
"""Deterministic scaffolding for the agentic SDLC pipeline.

Two commands:

  init      Create the artifact tree in a target repository, place the
            documented format templates, and (if absent) write a starter
            sdlc.config.yaml skeleton. Idempotent: existing files are skipped
            unless --force is given.

  validate  Validate a target repository's sdlc.config.yaml against the
            profile model, and check the artifact tree is complete. Prints a
            JSON report.

The setup skill drives this CLI. The agent decides the profile values; this
script guarantees the mechanical scaffolding is exact and repeatable.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, ValidationError


# ---------------------------------------------------------------------------
# Profile model (authoritative validator for sdlc.config.yaml)
# ---------------------------------------------------------------------------


class Project(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str
    description: str = ""
    kind: Literal["greenfield", "brownfield"]


class Task(BaseModel):
    model_config = ConfigDict(extra="allow")

    id_scheme: str = "TASK-{NNN}"
    spec_grouping: str = "by-concern"


class Vcs(BaseModel):
    model_config = ConfigDict(extra="allow")

    default_base_branch: str = "master"
    branch_scheme: str = "feature/{task-id-lower}-{slug}"


class TechStack(BaseModel):
    model_config = ConfigDict(extra="allow")

    language: str
    package_manager: str = ""


class TestGate(BaseModel):
    model_config = ConfigDict(extra="allow")

    commands: list[str] = Field(default_factory=list)
    conventions_doc: str = "reference/testing-conventions.md"
    test_naming: str = "test_{behaviour}"


class DeployConfig(BaseModel):
    model_config = ConfigDict(extra="allow")

    detected: bool = False
    config_files: list[str] = Field(default_factory=list)


class Reference(BaseModel):
    model_config = ConfigDict(extra="allow")

    context_doc: str = "reference/CONTEXT.md"
    adr_dir: str = "reference/adr"


class Review(BaseModel):
    model_config = ConfigDict(extra="allow")

    mode: Literal["light", "thorough"] = "thorough"
    roster: list[str] = Field(default_factory=list)
    consolidator: str = "review-consolidator"
    severity_model: str = "irreversibility x silence x blast-radius"


class FailurePatterns(BaseModel):
    model_config = ConfigDict(extra="allow")

    state_consistency: list = Field(default_factory=list)
    trust_boundary: list = Field(default_factory=list)
    observability: list = Field(default_factory=list)
    robustness: list = Field(default_factory=list)
    live_path_wiring: list = Field(default_factory=list)


class SubsystemIndex(BaseModel):
    model_config = ConfigDict(extra="allow")

    enabled: bool = False
    path: str | None = None


class SdlcConfig(BaseModel):
    model_config = ConfigDict(extra="allow")

    project: Project
    artifact_root: str = "ai_docs"
    task: Task = Field(default_factory=Task)
    vcs: Vcs = Field(default_factory=Vcs)
    tech_stack: TechStack
    test_gate: TestGate = Field(default_factory=TestGate)
    deploy_config: DeployConfig = Field(default_factory=DeployConfig)
    reference: Reference = Field(default_factory=Reference)
    review: Review = Field(default_factory=Review)
    failure_patterns: FailurePatterns = Field(default_factory=FailurePatterns)
    subsystem_index: SubsystemIndex = Field(default_factory=SubsystemIndex)


# ---------------------------------------------------------------------------
# Tree definition
# ---------------------------------------------------------------------------

DIRECTORIES: list[str] = [
    "specs",
    "reference",
    "reference/adr",
    "diagrams",
    "task-briefs",
    "explorations",
    "reviews",
    "walkthroughs",
    "reconciliations",
]

# Singleton documents placed once at the artifact root, copied from a template.
SINGLETONS: dict[str, str] = {
    "specs/index.md": "specs-index.md",
    "reference/CONTEXT.md": "CONTEXT.md",
    "reference/testing-conventions.md": "testing-conventions.md",
    "runbook.md": "runbook.md",
    "charter.md": "charter.md",
    "prd.md": "prd.md",
    "architecture.md": "architecture.md",
    "implementation-plan.md": "implementation-plan.md",
}

# Per-directory README files documenting the artifact format, copied from a
# template. A value of None means the README text is generated below.
DIR_READMES: dict[str, str | None] = {
    "specs": "spec.md",
    "reference/adr": "adr.md",
    "task-briefs": "task-brief.md",
    "explorations": "exploration.md",
    "reviews": "review.md",
    "walkthroughs": "walkthrough.md",
    "reconciliations": "reconciliation.md",
    "diagrams": None,
}

GENERATED_READMES: dict[str, str] = {
    "diagrams": (
        "# Diagrams\n\n"
        "Architecture and data-flow diagrams produced in the architecture phase. "
        "Prefer text-based formats (for example Mermaid `.mmd`) so they are diffable.\n"
    ),
}

DEFAULT_ROSTER: list[str] = [
    "spec-conformance",
    "correctness",
    "state-and-concurrency",
    "security-and-trust-boundary",
    "failure-and-robustness",
    "observability",
    "test-adequacy",
    "interface-and-data-integrity",
    "conventions",
]


def config_skeleton(artifact_root: str) -> str:
    """A starter sdlc.config.yaml for the setup agent to fill with real values."""
    roster_lines: str = "\n".join(f"    - {dimension}" for dimension in DEFAULT_ROSTER)
    skeleton: str = f"""# sdlc.config.yaml
# Generated skeleton. The setup skill fills these values from the greenfield
# interview or the brownfield scan. See .claude/config/sdlc.config.schema.yaml
# for the documented shape and .claude/config/examples for worked examples.

project:
  name: TODO
  description: TODO
  kind: TODO  # greenfield | brownfield

artifact_root: {artifact_root}

task:
  id_scheme: "TASK-{{NNN}}"
  spec_grouping: by-concern

vcs:
  default_base_branch: master
  branch_scheme: "feature/{{task-id-lower}}-{{slug}}"

tech_stack:
  language: TODO
  package_manager: TODO

test_gate:
  commands: []
  conventions_doc: reference/testing-conventions.md
  test_naming: "test_{{behaviour}}"

deploy_config:
  detected: false
  config_files: []

reference:
  context_doc: reference/CONTEXT.md
  adr_dir: reference/adr

review:
  mode: thorough
  roster:
{roster_lines}
  consolidator: review-consolidator
  severity_model: "irreversibility x silence x blast-radius"

failure_patterns:
  state_consistency: []
  trust_boundary: []
  observability: []
  robustness: []
  live_path_wiring: []

subsystem_index:
  enabled: false
  path: null
"""
    return skeleton


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def templates_dir() -> Path:
    """The templates directory, resolved relative to this script."""
    resolved: Path = Path(__file__).resolve().parent.parent / "templates"
    return resolved


def read_template(name: str) -> str:
    path: Path = templates_dir() / name
    if not path.exists():
        raise FileNotFoundError(f"template not found: {path}")
    content: str = path.read_text(encoding="utf-8")
    return content


def write_if_absent(
    target: Path,
    content: str,
    force: bool,
    created: list[str],
    skipped: list[str],
) -> None:
    if target.exists() and not force:
        skipped.append(str(target))
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    created.append(str(target))


def resolve_artifact_root(root: Path, explicit: str | None) -> str:
    """Prefer the explicit flag, then an existing config, then the default."""
    if explicit is not None:
        return explicit
    config_path: Path = root / "sdlc.config.yaml"
    if config_path.exists():
        try:
            loaded: dict = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
            candidate = loaded.get("artifact_root")
            if isinstance(candidate, str) and candidate:
                return candidate
        except yaml.YAMLError:
            pass
    return "ai_docs"


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------


def cmd_init(args: argparse.Namespace) -> int:
    root: Path = Path(args.root).resolve()
    artifact_root: str = resolve_artifact_root(root, args.artifact_root)
    base: Path = root / artifact_root
    created: list[str] = []
    skipped: list[str] = []

    for directory in DIRECTORIES:
        (base / directory).mkdir(parents=True, exist_ok=True)

    for rel_dest, template_name in SINGLETONS.items():
        content: str = read_template(template_name)
        write_if_absent(base / rel_dest, content, args.force, created, skipped)

    for directory, template_name in DIR_READMES.items():
        if template_name is None:
            content = GENERATED_READMES[directory]
        else:
            content = read_template(template_name)
        write_if_absent(base / directory / "README.md", content, args.force, created, skipped)

    if not args.no_config_skeleton:
        write_if_absent(
            root / "sdlc.config.yaml",
            config_skeleton(artifact_root),
            args.force,
            created,
            skipped,
        )

    report: dict = {
        "command": "init",
        "root": str(root),
        "artifact_root": artifact_root,
        "created": created,
        "skipped": skipped,
    }
    print(json.dumps(report, indent=2))
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    root: Path = Path(args.root).resolve()
    config_path: Path = root / "sdlc.config.yaml"
    errors: list[str] = []
    missing_paths: list[str] = []

    if not config_path.exists():
        report: dict = {
            "command": "validate",
            "root": str(root),
            "valid": False,
            "errors": [f"sdlc.config.yaml not found at {config_path}"],
            "missing_paths": [],
        }
        print(json.dumps(report, indent=2))
        return 1

    artifact_root: str = "ai_docs"
    try:
        loaded: dict = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
        config: SdlcConfig = SdlcConfig.model_validate(loaded)
        artifact_root = config.artifact_root
    except yaml.YAMLError as exc:
        errors.append(f"YAML parse error: {exc}")
    except ValidationError as exc:
        for issue in exc.errors():
            location: str = ".".join(str(part) for part in issue["loc"])
            errors.append(f"{location}: {issue['msg']}")

    base: Path = root / artifact_root
    for directory in DIRECTORIES:
        if not (base / directory).is_dir():
            missing_paths.append(str(base / directory))
    for rel_dest in SINGLETONS:
        if not (base / rel_dest).exists():
            missing_paths.append(str(base / rel_dest))

    valid: bool = not errors and not missing_paths
    report = {
        "command": "validate",
        "root": str(root),
        "artifact_root": artifact_root,
        "valid": valid,
        "errors": errors,
        "missing_paths": missing_paths,
    }
    print(json.dumps(report, indent=2))
    return 0 if valid else 1


def build_parser() -> argparse.ArgumentParser:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog="scaffold.py",
        description="Scaffold and validate the agentic SDLC artifact tree.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Create the artifact tree.")
    init_parser.add_argument("--root", default=".", help="Target repository root.")
    init_parser.add_argument(
        "--artifact-root",
        default=None,
        help="Artifact root directory name. Defaults to existing config or ai_docs.",
    )
    init_parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files.",
    )
    init_parser.add_argument(
        "--no-config-skeleton",
        action="store_true",
        help="Do not write a starter sdlc.config.yaml.",
    )
    init_parser.set_defaults(func=cmd_init)

    validate_parser = subparsers.add_parser("validate", help="Validate config and tree.")
    validate_parser.add_argument("--root", default=".", help="Target repository root.")
    validate_parser.set_defaults(func=cmd_validate)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser: argparse.ArgumentParser = build_parser()
    args: argparse.Namespace = parser.parse_args(argv)
    exit_code: int = args.func(args)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
