---
name: sdlc
description: Overview and entry point for the agentic SDLC pipeline. Use to understand the phases, decide which phase skill to run next, and see the artifact layout and how tasks are tracked.
---

# Agentic SDLC

A portable, self-contained software development lifecycle pipeline, driven phase by phase from project vision through to reviewed, reconciled implementation. The pipeline is a project-agnostic spine plus one per-project configuration file, `sdlc.config.yaml`, at the repository root. Every agent reads its slice of that profile. Nothing is hardcoded per project.

## The unit of work

The unit of work is a flat task (`TASK-001`, `TASK-002`). There is no epic or story hierarchy. Spec documents under the artifact root group tasks by area of concern, for readability only.

## Tracking

There is no external tracker. All tracking lives in the artifact tree. The task registry and status board is `<artifact_root>/specs/index.md`, where `<artifact_root>` is the configured `artifact_root` (default `ai_docs`).

## Phases and which skill to run

- Setup, once, after the framework is copied in: run the `setup` skill. Creates the artifact tree and writes `sdlc.config.yaml`.
- Phase 0, charter: run the `initialise-project` skill. Produces `charter.md`.
- Phase 1, requirements: run the `define-requirements` skill. Produces `prd.md`.
- Phase 2, architecture: run the `design-architecture` skill. Produces `architecture.md`, diagrams, the domain glossary, and decision records.
- Phase 3, plan: run the `plan-implementation` skill. Produces the spec documents `specs/NN-<area>.md` and the task registry `specs/index.md`. This is the join into the implementation loop.
- Phase 4, implement a task: run the `implement-task` skill for a task id. It explores, prepares, implements, runs the review panel, consolidates, walks through, and reconciles.

The front half (phases 0 to 3) is interactive: the skills converse with you and may spawn research subagents. The back half (phase 4) is headless: an orchestration skill drives subagents that report evidence and never converse.

## Artifact tree

```
<artifact_root>/
  charter.md                      phase 0
  prd.md                          phase 1
  architecture.md                 phase 2
  implementation-plan.md          phase 3
  diagrams/                       phase 2
  specs/
    index.md                      task registry and status board
    NN-<area>.md                  spec documents, contain tasks
  reference/
    CONTEXT.md                    domain glossary
    testing-conventions.md
    adr/                          architectural decision records
    <domain>.md                   created as needed
  task-briefs/<task-id>.md
  explorations/<task-id>.md
  reviews/<task-id>/<dimension>.md and consolidated.md
  walkthroughs/<task-id>.md
  reconciliations/<task-id>.md
  runbook.md
```

## Code review

Code review is a standard stage of `implement-task`, not an optional extra. A panel of reviewers (one `code-reviewer` per dimension in `review.roster`) runs in parallel, then `review-consolidator` produces the authoritative verdict. The panel can also be run standalone on an existing change.
