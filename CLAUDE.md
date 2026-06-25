# Working on the agentic-sdlc repository

This repository is the source of truth for a portable agentic software development lifecycle pipeline. Read `DESIGN.md` before changing anything structural.

## Core principle

The pipeline is a project-agnostic spine plus a single per-project configuration file. The spine (everything under `.claude/`) is copied verbatim into a target repository and never edited per project. Every project-specific fact lives in `sdlc.config.yaml` at the target repository root, generated at setup. No agent, skill, or script may hardcode a project specific (paths, branch names, test commands, tech stack, story prefixes). All of these are read from the profile.

## What reads what

- Every agent reads `sdlc.config.yaml` and resolves its slice: `artifact_root` (default `ai_docs`), `task.id_scheme`, `vcs.default_base_branch`, `test_gate.commands`, `reference.context_doc`, `reference.adr_dir`, `review.roster` and `review.mode`, `failure_patterns`, `subsystem_index`.
- All artifacts live under the configured `artifact_root`. Examples in prose use `ai_docs/`, but the value is always the configured root.

## Conventions

- Python throughout. `uv` for running, Pydantic V2 for all data models, full type hints. No Node.
- British English spelling.
- No em-dashes, and no hyphens used as sentence punctuation. Hyphens are fine only in their grammatical role (compound words).
- `master` is the default branch name.
- No external trackers, no `gh` CLI, no CI merge gate, no three-surface sync. The artifact tree is the system of record. `specs/index.md` is the task registry.
- Any structured output an agent must emit for downstream parsing uses XML tags parsed by tolerant regex, never strict JSON. Most artifacts are markdown documents.

## The unit of work

A flat task (`TASK-NNN`). No epics or stories inside the pipeline. Spec documents group tasks by area for readability only.

## Authoring agents and skills

- Agent frontmatter: `name`, `description` (literal block scalar), `tools`, `model: opus`. Only list `Write` or `Edit` for an agent that legitimately writes its own report or, for the reconciler, updates specs and reference docs. Never give an agent write access to source code.
- Skill frontmatter: `name` and `description` only. Skills run interactively in the main context.
- Front half (initialise, requirements, architecture, plan) are interactive skills that converse with the developer and may spawn research subagents.
- Back half (implement-task) is an orchestration skill that drives headless subagents which report evidence and never converse.
- Each agent's inline output format must match the corresponding template under `.claude/templates/`.

## Layout

- `.claude/agents/` the subagents.
- `.claude/skills/` the skills, one directory each with a `SKILL.md`.
- `.claude/commands/` thin slash-command wrappers.
- `.claude/scripts/` the Python CLIs (the deterministic scaffolding).
- `.claude/config/` the profile schema and worked examples.
- `.claude/templates/` the artifact format templates placed into a target's artifact tree at setup.
- `install.sh` the bootstrap that copies `.claude/` into a target repository.
- `docs/` documentation about the framework itself, not copied into targets.
