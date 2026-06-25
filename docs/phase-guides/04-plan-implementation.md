# Phase 3: Plan Implementation

## Purpose

Phase 3 is the join between the two halves of the pipeline. The front half elicited what to build and how it is shaped; the back half drives each task through the implementation loop. This phase connects them: it emits exactly what the loop consumes, the spec documents and the task registry. The loop assumes these already exist; this phase produces them. It turns the architecture and the requirements into a human-readable implementation plan, a set of spec documents grouped by area of concern, and the registry that maps each task to its spec and tracks its status.

This is an interactive phase. It converses with the developer to settle the plan, then spawns subagents to do the heavy decomposition into tasks, and assembles the registry from what they return.

## Inputs

- `sdlc.config.yaml`, resolved first, for `artifact_root` (default `ai_docs`) and `task.id_scheme` (default `TASK-{NNN}`, the shape of a task id used when assigning ids in the registry).
- `<artifact_root>/architecture.md`, the phase 2 output, read in full: the components, boundaries, integration points, and settled technical decisions.
- `<artifact_root>/prd.md`, the phase 1 output, read in full: the requirement identifiers and their MoSCoW priorities, so every task traces back to the requirements it serves.

If `sdlc.config.yaml` is absent, the skill notes it, falls back to the defaults, and proceeds.

## What it produces

Three outputs, under the configured `artifact_root` (default `ai_docs`):

- `<artifact_root>/implementation-plan.md`, the plan, matching `.claude/templates/implementation-plan.md`. Its sections are the approach, the work breakdown, sequencing and dependencies, the first deliverable, the testing strategy, and the risks.
- `<artifact_root>/specs/NN-<area>.md`, one spec document per area of concern, each containing its tasks, matching `.claude/templates/spec.md`. Each task carries an objective, requirements split into must, should, and out of scope, acceptance criteria in Given/When/Then form, dependencies, and the requirement identifiers it serves.
- `<artifact_root>/specs/index.md`, the task registry: one row per task, the map from task id to spec document, and the status board, matching `.claude/templates/specs-index.md`. This is the system of record. There is no external tracker.

The unit of work is a flat task, for example `TASK-001`. There are no epics and no stories inside the pipeline. Spec documents group tasks by area of concern for readability only; the grouping is file organisation, not a hierarchy level.

## How to run

- Command: `/plan-implementation`.
- Skill: `plan-implementation`.
- Agents spawned: `plan-decomposer` subagents, one per area of concern, to decompose each area into tasks and write its spec document.

The skill reads the architecture and the requirements, then interviews the developer across the checklist: the work breakdown, the areas of concern, sequencing and dependencies, the first deliverable, the testing strategy, and the risks. It writes the implementation plan, then spawns one `plan-decomposer` per area in a single batch. Each decomposer is given its area name and spec document number, the relevant slice of the architecture and the requirement identifiers, and the sequencing decisions that touch its area. It carves the area into flat, vertical-slice tasks, each sized to flow through the implementation loop in one pass, writes its spec document, and returns its ordered task list. The decomposers do not assign global ids. After every decomposer completes, the skill assembles the registry: it assigns flat task ids in a single global sequence across all areas, respecting the dependency ordering where it can, sets every task's status to `planned`, sets the artifact columns to `-`, and then updates each spec document so its task headings carry the assigned global ids. The spec documents and the registry must agree on every id.

## What good output looks like

- The task ids are a single global sequence across all spec documents. The second area does not restart at `TASK-001`.
- The spec documents and the registry agree on every id and every cross-task dependency reference.
- Each task is a complete vertical slice of behaviour, testable on its own, not a horizontal layer that delivers nothing alone. Each is small enough for one pass through the loop and large enough to stand alone.
- Every task traces back to the requirement identifiers it serves.
- A concrete first deliverable is named: the thinnest end-to-end slice that demonstrates the system working, and the tasks it comprises. This replaces sprint ceremony.
- The sequence respects the dependencies, so a task generally appears after the tasks it depends on.
- Every task is at status `planned`, because no phase has run at planning time.
- Decisions already settled in the architecture and the requirements are built on, not reopened.

## Hand-off

Phase 4, `implement-task`, consumes the registry. The registry is the entry point: the loop resolves a task's spec document by looking the task up in `specs/index.md`, then drives it through explore, prepare, implement, review panel, consolidate, walkthrough, and reconcile, advancing the task's status in the registry as each phase completes. Each task can be driven independently, in the order the sequencing established. This is the single seam between planning and building: everything before it is conversation and documents, everything after it is the per-task loop.
