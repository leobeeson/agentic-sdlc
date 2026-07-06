# /// script
# requires-python = ">=3.11"
# dependencies = ["pydantic>=2", "pyyaml"]
# ///
"""Deterministic scaffolding for the agentic SDLC shared memory.

Three commands:

  init            Create the two-tier artefact tree in a target repository (the
                  project spine plus the initiatives root), place the spine
                  singletons from the templates, and (if absent) write a starter
                  sdlc.config.yaml skeleton. Idempotent: existing files are
                  skipped unless --force is given.

  new-initiative  Mint one initiative workspace under
                  <artefact-root>/initiatives/<initiative-id>/ with its
                  subdirectories and task registry, and append the initiative to
                  the initiative registry when the registry exists.

  validate        Validate sdlc.config.yaml against the profile model and check
                  the spine is complete. Prints a JSON report.

The setup skill drives `init`; the orchestrator drives `new-initiative` when it
mints an initiative at plan composition. The agent decides the profile values;
this script guarantees the mechanical scaffolding is exact and repeatable.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, ValidationError


# ---------------------------------------------------------------------------
# Profile model (authoritative validator for sdlc.config.yaml)
# ---------------------------------------------------------------------------

MANDATORY_AGENT_ROLES: tuple[str, ...] = (
    "review-consolidator",
    "reconciler",
)

REVIEWER_DIMENSIONS: tuple[str, ...] = (
    "spec-conformance",
    "correctness",
    "state-and-concurrency",
    "security-and-trust-boundary",
    "failure-and-robustness",
    "observability",
    "test-adequacy",
    "interface-and-data-integrity",
    "conventions",
    "guidelines",
)


class Project(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str
    kind: Literal["data-engineering", "application", "library", "tooling"]
    stack: list[str] = Field(default_factory=list)
    base_branch: str = "main"


class ArtefactTree(BaseModel):
    model_config = ConfigDict(extra="allow")

    root: str = "ai_docs/"


class ProductLocations(BaseModel):
    model_config = ConfigDict(extra="allow")

    adp_foundry_yaml: str | None = None
    dbt_project: str | None = None
    code_root: str | None = None


class Validation(BaseModel):
    model_config = ConfigDict(extra="allow")

    commands: list[str] = Field(default_factory=list)


class Review(BaseModel):
    model_config = ConfigDict(extra="allow")

    severity_model: Literal["three-tier"] = "three-tier"
    roster: list[str] = Field(default_factory=list)


class SdlcConfig(BaseModel):
    model_config = ConfigDict(extra="allow")

    project: Project
    artefact_tree: ArtefactTree = Field(default_factory=ArtefactTree)
    product_locations: ProductLocations = Field(default_factory=ProductLocations)
    validation: Validation = Field(default_factory=Validation)
    review: Review = Field(default_factory=Review)
    failure_patterns: str = ".claude/config/failure-patterns.yaml"
    schema_profile: Literal["core", "data-engineering"] = "core"
    agents: dict[str, str | dict[str, str]] = Field(default_factory=dict)


def availability_errors(config: SdlcConfig) -> list[str]:
    """Reject a configuration that disables a mandatory agent role.

    The review of a generated change with its consolidation, the reconciliation
    check, and the run record are mandatory in every composition that changes
    the product; the availability switch cannot remove them.
    """
    errors: list[str] = []
    for role_name, setting in config.agents.items():
        disabled_globally: bool = setting == "disabled" or (
            isinstance(setting, dict) and setting.get("default") == "disabled"
        )
        if not disabled_globally:
            continue
        if role_name in MANDATORY_AGENT_ROLES or role_name.startswith("reviewer-"):
            errors.append(
                f"agents.{role_name}: a mandatory stage cannot be disabled "
                "(review with its consolidation, and reconciliation, are immune "
                "to the availability switch)"
            )
    for dimension in config.review.roster:
        if dimension not in REVIEWER_DIMENSIONS:
            errors.append(
                f"review.roster: unknown reviewer dimension '{dimension}' "
                f"(known: {', '.join(REVIEWER_DIMENSIONS)})"
            )
    return errors


# ---------------------------------------------------------------------------
# Tree definition
# ---------------------------------------------------------------------------

# Tier 1, the project spine: singular, durable, updated in place.
SPINE_DIRECTORIES: list[str] = [
    "reference",
    "reference/adrs",
    "reference/guidelines",
    "diagrams",
    "data-engineering",
    "initiatives",
]

# Spine singletons placed once, copied from the templates.
SPINE_SINGLETONS: dict[str, str] = {
    "reference/CONTEXT.md": "CONTEXT.md",
    "reference/testing-conventions.md": "testing-conventions.md",
    "initiatives/index.md": "initiative-index.md",
    "runbook.md": "runbook.md",
}

# Tier 2, one workspace per initiative.
INITIATIVE_DIRECTORIES: list[str] = [
    "specs",
    "explorations",
    "task-briefs",
    "reviews",
    "walkthroughs",
    "reconciliations",
    "run-record",
]

INITIATIVE_ID_PATTERN: re.Pattern[str] = re.compile(r"^INIT-\d{3,}(-[a-z0-9][a-z0-9-]*)?$")


def config_skeleton(artefact_root: str) -> str:
    """A starter sdlc.config.yaml for the setup skill to fill with real values."""
    skeleton: str = f"""# sdlc.config.yaml
# Generated skeleton. The setup skill fills these values from the greenfield
# interview or the brownfield survey. See .claude/config/sdlc.config.schema.yaml
# for the documented shape and .claude/config/examples/ for worked examples.

project:
  name: TODO
  kind: TODO            # data-engineering | application | library | tooling
  stack: []             # e.g. [adp-foundry, dbt, python]
  base_branch: main

artefact_tree:
  root: {artefact_root}

product_locations:
  # adp_foundry_yaml: TODO   # the directory the Airflow deployment scans
  # dbt_project: TODO        # the dbt project root; models under models/
  code_root: src/

validation:
  commands: []          # the real commands the testing loop runs

review:
  severity_model: three-tier
  roster:
    - spec-conformance
    - correctness
    - failure-and-robustness
    - test-adequacy
    - conventions

failure_patterns: .claude/config/failure-patterns.yaml
schema_profile: core    # core | data-engineering

agents: {{}}
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


def resolve_artefact_root(root: Path, explicit: str | None) -> str:
    """Prefer the explicit flag, then an existing config, then the default."""
    if explicit is not None:
        return explicit
    config_path: Path = root / "sdlc.config.yaml"
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


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------


def cmd_init(args: argparse.Namespace) -> int:
    root: Path = Path(args.root).resolve()
    artefact_root: str = resolve_artefact_root(root, args.artefact_root)
    base: Path = root / artefact_root
    created: list[str] = []
    skipped: list[str] = []

    for directory in SPINE_DIRECTORIES:
        (base / directory).mkdir(parents=True, exist_ok=True)

    for rel_dest, template_name in SPINE_SINGLETONS.items():
        content: str = read_template(template_name)
        write_if_absent(base / rel_dest, content, args.force, created, skipped)

    if not args.no_config_skeleton:
        skeleton: str = config_skeleton(artefact_root + "/")
        write_if_absent(
            root / "sdlc.config.yaml",
            skeleton,
            args.force,
            created,
            skipped,
        )

    report: dict = {
        "command": "init",
        "root": str(root),
        "artefact_root": artefact_root,
        "created": created,
        "skipped": skipped,
    }
    print(json.dumps(report, indent=2))
    return 0


def cmd_new_initiative(args: argparse.Namespace) -> int:
    root: Path = Path(args.root).resolve()
    artefact_root: str = resolve_artefact_root(root, args.artefact_root)
    initiative_id: str = args.initiative_id

    if not INITIATIVE_ID_PATTERN.match(initiative_id):
        report_invalid: dict = {
            "command": "new-initiative",
            "valid": False,
            "errors": [
                f"initiative id '{initiative_id}' does not match INIT-NNN[-slug] "
                "(e.g. INIT-042-orders-ingestion)"
            ],
        }
        print(json.dumps(report_invalid, indent=2))
        return 1

    workspace: Path = root / artefact_root / "initiatives" / initiative_id
    created: list[str] = []
    skipped: list[str] = []

    for directory in INITIATIVE_DIRECTORIES:
        target_dir: Path = workspace / directory
        if target_dir.is_dir():
            skipped.append(str(target_dir))
        else:
            target_dir.mkdir(parents=True, exist_ok=True)
            created.append(str(target_dir))

    registry_content: str = read_template("specs-index.md")
    write_if_absent(workspace / "specs" / "index.md", registry_content, False, created, skipped)

    report: dict = {
        "command": "new-initiative",
        "initiative_id": initiative_id,
        "workspace": str(workspace),
        "created": created,
        "skipped": skipped,
        "note": (
            "the orchestrator, the single writer of initiatives/index.md, appends "
            "this initiative's status sentence itself"
        ),
    }
    print(json.dumps(report, indent=2))
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    root: Path = Path(args.root).resolve()
    config_path: Path = root / "sdlc.config.yaml"
    errors: list[str] = []
    missing_paths: list[str] = []

    if not config_path.exists():
        report_missing: dict = {
            "command": "validate",
            "root": str(root),
            "valid": False,
            "errors": [f"sdlc.config.yaml not found at {config_path}"],
            "missing_paths": [],
        }
        print(json.dumps(report_missing, indent=2))
        return 1

    artefact_root: str = "ai_docs"
    try:
        loaded: dict = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
        config: SdlcConfig = SdlcConfig.model_validate(loaded)
        artefact_root = config.artefact_tree.root.rstrip("/")
        switch_errors: list[str] = availability_errors(config)
        errors.extend(switch_errors)
    except yaml.YAMLError as exc:
        errors.append(f"YAML parse error: {exc}")
    except ValidationError as exc:
        for issue in exc.errors():
            location: str = ".".join(str(part) for part in issue["loc"])
            errors.append(f"{location}: {issue['msg']}")

    base: Path = root / artefact_root
    for directory in SPINE_DIRECTORIES:
        if not (base / directory).is_dir():
            missing_paths.append(str(base / directory))
    for rel_dest in SPINE_SINGLETONS:
        if not (base / rel_dest).exists():
            missing_paths.append(str(base / rel_dest))

    valid: bool = not errors and not missing_paths
    report: dict = {
        "command": "validate",
        "root": str(root),
        "artefact_root": artefact_root,
        "valid": valid,
        "errors": errors,
        "missing_paths": missing_paths,
    }
    print(json.dumps(report, indent=2))
    return 0 if valid else 1


def build_parser() -> argparse.ArgumentParser:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog="scaffold.py",
        description="Scaffold and validate the agentic SDLC shared memory.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Create the project spine.")
    init_parser.add_argument("--root", default=".", help="Target repository root.")
    init_parser.add_argument(
        "--artefact-root",
        default=None,
        help="Artefact root directory name. Defaults to existing config or ai_docs.",
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

    new_initiative_parser = subparsers.add_parser(
        "new-initiative",
        help="Mint one initiative workspace under initiatives/.",
    )
    new_initiative_parser.add_argument("initiative_id", help="e.g. INIT-042-orders-ingestion")
    new_initiative_parser.add_argument("--root", default=".", help="Target repository root.")
    new_initiative_parser.add_argument(
        "--artefact-root",
        default=None,
        help="Artefact root directory name. Defaults to existing config or ai_docs.",
    )
    new_initiative_parser.set_defaults(func=cmd_new_initiative)

    validate_parser = subparsers.add_parser("validate", help="Validate config and spine.")
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
