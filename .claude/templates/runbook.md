# Runbook

How to run the pipeline phases in this project. This is the operator reference for driving the agentic SDLC, including running phases outside an interactive Claude Code session.

## Setup

Once, after the framework is copied in:

- Run the `setup` skill (or `uv run .claude/scripts/scaffold.py init --root .`) to create the artifact tree and the `sdlc.config.yaml` skeleton, then fill the profile by interview or scan.
- Validate at any time with `uv run .claude/scripts/scaffold.py validate --root .`.

## Phases

- Phase 0, charter: run the `initialise-project` skill.
- Phase 1, requirements: run the `define-requirements` skill.
- Phase 2, architecture: run the `design-architecture` skill.
- Phase 3, plan: run the `plan-implementation` skill. Produces the spec documents and the task registry.
- Phase 4, implement a task: run the `implement-task` skill for a task id. It explores, prepares, implements, runs the review panel, consolidates, walks through, and reconciles.

## Invoking individual agents

Each implementation-phase agent can be run on its own, for example the `feature-explorer` for an ad-hoc investigation, or the review panel standalone on an existing change. See the skill files for the exact invocation strings.
