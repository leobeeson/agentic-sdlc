# Agentic SDLC

A portable, self-contained agentic software development lifecycle pipeline. It is a set of Claude Code agents, skills, commands, and supporting Python tooling that a team copies into any project repository and then drives end to end: from project vision through requirements, architecture, planning, implementation, and code review.

## What it is

The pipeline ships as a project-agnostic spine. Every project-specific fact lives in a single configuration file, `sdlc.config.yaml`, generated once at setup and read in slices by every agent. The spine is never edited per project. The intent is ad-hoc spec-driven development that works the same way in any repository.

The full design rationale is in `DESIGN.md`. Working guidance for this repository is in `CLAUDE.md`. End-user documentation is under `docs/`.

## Quick start

From this repository, copy the framework into a target repository:

```
./install.sh /path/to/target-repo
```

Then, inside the target repository, open Claude Code (or restart the session so the new agents and skills register) and run the setup skill:

```
/setup
```

Setup creates the complete, documented artifact tree and writes `sdlc.config.yaml` (greenfield interview, or brownfield scan of the existing repository). After that, drive the pipeline phase by phase with the skills:

1. `initialise-project` writes the charter.
2. `define-requirements` writes the requirements document.
3. `design-architecture` writes the architecture and decision records.
4. `plan-implementation` writes the spec documents and the task registry.
5. `implement-task` runs the per-task loop: explore, prepare, implement, review, walkthrough, reconcile.

## The unit of work

The unit of work in the implementation phase is a flat task (`TASK-001`, `TASK-002`). There is no epic or story hierarchy inside the pipeline. Spec documents under the artifact root group tasks by area of concern, for readability only.

## Tracking

The pipeline is completely self-contained. There is no synchronisation to any external tracker. All tracking lives inside the artifact tree as files. `specs/index.md` is the task registry and status board.
