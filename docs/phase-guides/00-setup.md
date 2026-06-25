# Setup

## Purpose

Setup prepares a repository to run the pipeline. It runs once, immediately after the framework has been copied in by `install.sh`, and it leaves the repository ready for phase 0. It does exactly two things: it creates the complete, documented artifact tree under the configured `artifact_root`, and it produces `sdlc.config.yaml` at the repository root, the single source of every project-specific fact that every agent reads thereafter.

Setup does not produce the charter. The charter is phase 0, authored later by `initialise-project`. The profile is how the project is built; the charter is what and why it is built. Setup establishes the how.

## Inputs

Setup is the first phase, so it reads no prior pipeline artifact. It reads:

- The repository itself, to decide whether the project is greenfield or brownfield. A quick scan with Glob and Read looks for source files, a dependency manifest, a test suite, CI configuration, and deployment configuration, ignoring the freshly copied `.claude/` framework and the scaffolded artifact tree.
- For the brownfield path, the existing codebase in depth: manifests, lockfiles, config files, CI workflows, git metadata, and source idioms cited at `file:line`. The `profile-discoverer` agent reads these to draft the profile from evidence.
- `.claude/config/sdlc.config.schema.yaml` for the documented shape of each profile field, and `.claude/config/examples/` for worked examples.

## What it produces

Two things, under the configured `artifact_root` (default `ai_docs`) and at the repository root.

- The complete artifact tree under `artifact_root`, created by `.claude/scripts/scaffold.py init`:
  - The directories `specs/`, `reference/`, `reference/adr/`, `diagrams/`, `task-briefs/`, `explorations/`, `reviews/`, `walkthroughs/`, `reconciliations/`.
  - The singleton documents `specs/index.md` (the task registry), `reference/CONTEXT.md`, `reference/testing-conventions.md`, `runbook.md`, and the phase output stubs `charter.md`, `prd.md`, `architecture.md`, `implementation-plan.md`.
  - A `README.md` in each artifact directory documenting that directory's purpose and the format of the artifacts it holds.
- `sdlc.config.yaml` at the repository root. The scaffolder writes a skeleton with `TODO` placeholders; the setup skill fills it with confirmed values and leaves no `TODO` behind.

The scaffolding is idempotent. Existing files are skipped, not overwritten, unless `--force` is passed.

## How to run

- Command: `/setup`.
- Skill: `setup`.
- Agents spawned: `profile-discoverer`, on the brownfield path only.

The skill follows this sequence:

- Scaffold the tree with `uv run .claude/scripts/scaffold.py init --root .`. The script declares its dependencies inline, so `uv run` resolves them with no separate install step. It prints a JSON report of what was created and what was skipped.
- Determine greenfield or brownfield by a quick scan, state the assessment, and confirm it with the developer. The developer's answer is authoritative.
- Gather the profile values. On the greenfield path, interview the developer for the project facts, the tech stack, the test gate commands, the base branch, the deployment surface, and the review mode and roster. On the brownfield path, spawn `profile-discoverer` to scan the repository and draft the profile from evidence, then walk the draft with the developer field by field.
- Write the confirmed values into `sdlc.config.yaml`, replacing every `TODO`.
- Validate with `uv run .claude/scripts/scaffold.py validate --root .`, which checks the config against the profile model and the tree for completeness. Fix and re-run until it reports valid.
- Report the final state and point the developer at `initialise-project`.

## What good output looks like

- The validate command reports `valid: true`, with no errors and no missing paths.
- `sdlc.config.yaml` carries no `TODO` placeholder. Every field holds a real value or a deliberate default.
- The test gate commands are the exact commands that run the suite, not an approximation. On the brownfield path these are copied verbatim from CI or the manifest, because reviewers run them as given.
- The base branch is the project's real default branch, detected from git on the brownfield path, not assumed.
- On the brownfield path, every populated field traces to concrete evidence, and the `profile-discoverer` has surfaced an explicit list of what it had to guess and what it could not determine, so the developer confirms before the profile is trusted.
- The artifact tree is complete and documented, so the developer sees the full structure up front rather than as it is filled lazily.

## Hand-off

Phase 0, `initialise-project`, consumes the result of setup. Every agent in every later phase reads its slice of `sdlc.config.yaml`, so the profile must be correct before any phase runs. The artifact tree gives every later phase the directories and templates it writes into. `initialise-project` reads `project.name`, `project.description`, and `project.kind` from the profile to seed the charter interview, and writes the charter into the `charter.md` stub that setup created.
