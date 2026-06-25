---
name: plan-implementation
description: Phase 3 of the agentic SDLC, the join between front-half planning and the back-half implementation loop. Use after the architecture and requirements exist, to turn them into an implementation plan, spec documents grouped by area of concern, and the task registry. Converses with the developer to settle the work breakdown, sequencing, the first deliverable, testing strategy, and risks, then spawns plan-decomposer subagents to write the specs and assembles the registry. Run this once the architecture is settled and you are ready to start building.
---

# Plan Implementation

Phase 3 of the pipeline, and the join between its two halves. The front half (initialise, requirements, architecture) elicits what to build and how it is shaped. The back half (`implement-task`) drives each task through explore, prepare, implement, review, walkthrough, and reconcile. This phase is what connects them: it emits exactly what the implementation loop consumes, the spec documents and the task registry. The loop assumes these already exist; this phase produces them.

This is an interactive skill. It converses with the developer to build the plan, then spawns `plan-decomposer` subagents to do the heavy decomposition into tasks, and assembles the task registry from what they return.

## What this skill reads from the profile

Everything project-specific is read at runtime from `sdlc.config.yaml` at the repository root. Resolve these before doing anything else. The defaults apply only when a field is absent.

- `artifact_root` (default `ai_docs`). All artifacts live under this tree. Prose below uses `ai_docs/`, but the value is always the configured root.
- `task.id_scheme` (default `TASK-{NNN}`). The shape of a task id, used when assigning ids in the registry.

If `sdlc.config.yaml` is absent, note it in your completion summary, fall back to the defaults, and proceed.

## Inputs and outputs

Reads:

- `<artifact_root>/architecture.md`, the phase 2 output.
- `<artifact_root>/prd.md`, the phase 1 output, for requirement identifiers (REQ-00X) and priorities.

Produces three outputs:

- `<artifact_root>/implementation-plan.md`, the plan.
- `<artifact_root>/specs/NN-<area>.md`, one spec document per area of concern, each containing its tasks.
- `<artifact_root>/specs/index.md`, the task registry: one row per task, the map from task id to spec document, and the status board. This is the system of record. There is no external tracker.

## The unit of work

A flat task, for example `TASK-001`. There are no epics and no stories inside the pipeline. Epic and story are product-planning language and stay in the requirements phase. Spec documents group tasks by area of concern for readability only; the grouping is file organisation, not a hierarchy level.

## Process

### 1. Read the architecture and requirements

Read `<artifact_root>/architecture.md` and `<artifact_root>/prd.md` in full. From the architecture, take the components, boundaries, integration points, and the technical decisions already settled. From the requirements, take the requirement identifiers and their MoSCoW priorities, so every task can be traced back to the requirements it serves. Do not reopen decisions already settled in the architecture; build the plan on top of them.

### 2. Interview the developer

Converse with the developer to settle the plan. This is the valuable core kept from the older planning consultant: a strong topic checklist, worked through interactively. Cover each of these, in roughly this order, confirming your understanding back to the developer as you go.

- **Work breakdown.** The set of concrete units of work needed to build what the architecture describes. Drive towards flat tasks that are each a coherent, testable slice.
- **Areas of concern.** How the tasks group into areas, one area per spec document (`specs/NN-<area>.md`). Group by area of the system, for example ingestion, storage, the API surface. This is a readability grouping, not a hierarchy.
- **Sequencing and dependencies.** The order tasks must be built in, and which tasks depend on which. Surface ordering forced by the architecture (a task cannot start before the thing it builds on exists).
- **First deliverable.** The smallest coherent set of tasks that produces something working end to end. This replaces agile sprint ceremony: instead of a time-boxed sprint, name the thinnest vertical slice that demonstrates the system working, and the tasks it comprises.
- **Testing strategy.** The levels of testing the work needs and how tasks will be verified, consistent with the conventions captured in `reference/testing-conventions.md`.
- **Risks.** What could go wrong, which tasks each risk affects, and the mitigation.

Ask focused questions, propose a structure rather than demanding the developer supply one from a blank page, and record decisions as you settle them. Do not pad the interview; once a topic is settled, move on.

### 3. Write the implementation plan

Write `<artifact_root>/implementation-plan.md` from the settled interview, matching the implementation-plan template. The sections are:

- **Approach.** The build strategy in a few sentences, including what the first deliverable is.
- **Work breakdown.** A table of areas of concern, each with its spec document `specs/NN-<area>.md` and the tasks within it.
- **Sequencing and dependencies.** The order tasks must be built in, and the dependencies between them.
- **First deliverable.** The smallest coherent set of tasks that produces something working end to end.
- **Testing strategy.** The levels of testing and the conventions captured in `reference/testing-conventions.md`.
- **Risks.** A table of risk, affected tasks, and mitigation.

The plan is the human-readable narrative. The machine-readable handoff is the spec documents and the registry, produced next.

### 4. Decompose each area into a spec document

For each area of concern in the work breakdown, spawn a `plan-decomposer` subagent to write the spec document `<artifact_root>/specs/NN-<area>.md` and return its task list. The decomposers do the heavy decomposition: turning an area into concrete flat tasks, each with an objective, requirements (must, should, out of scope), acceptance criteria in Given/When/Then form, dependencies, and the requirement identifiers it serves.

Spawn one decomposer per area. They are independent and can run concurrently, so spawn them in a single batch. Give each decomposer:

- The area name and its spec document number and path (`specs/NN-<area>.md`).
- The relevant slice of the architecture and the requirement identifiers the area serves.
- The sequencing and dependency decisions from the interview that touch the area.

Each decomposer writes its spec document matching the spec template and returns its ordered task list (each task with its short name, objective, dependencies, and serving requirement identifiers) for the registry. Wait for every decomposer to complete before assembling the registry.

Note on task ids: the decomposers describe the tasks within their area, but the global task ids are assigned by this skill in step 5, not by the decomposers. A decomposer works in terms of its own ordered list; the spec documents and registry receive their final ids when you assemble the registry. Apply the ids to each spec document after assignment so the spec and the registry agree.

### 5. Assemble the task registry

Assemble `<artifact_root>/specs/index.md` from the task lists returned by the decomposers, matching the specs-index template. One row per task.

Task id assignment rule: assign flat task ids in a single global sequence across all spec documents, `TASK-001`, `TASK-002`, `TASK-003`, and so on, following the configured `task.id_scheme`. This is a single global sequence, not per-area numbering: the second area does not restart at `TASK-001`. Walk the areas in spec-document order, and within each area in the decomposer's returned order, assigning the next id in the sequence to each task. Resolve the sequence so it respects the dependency ordering from the interview where it can, so a task generally appears after the tasks it depends on.

For every row:

- The task id, in the global sequence.
- The spec document it belongs to (`NN-<area>`), so every task points at its spec.
- The task name.
- Status `planned` for every task. No phase has run yet.
- The artifact columns (Brief, Exploration, Review, Walkthrough, Reconciliation) all set to `-`; the implementation-phase agents fill these as work proceeds.

After assigning ids, update each spec document so its `TASK-NNN` headings carry the assigned global ids and any cross-task dependency references match the registry. The spec documents and the registry must agree on every id.

## The handoff into implement-task

Once the registry exists, this phase is done and the implementation loop takes over. The registry is the entry point: `implement-task` resolves a task's spec document by looking the task up in `specs/index.md`, then drives it through explore, prepare, implement, review panel, consolidate, walkthrough, and reconcile, advancing the task's status in the registry as each phase completes. Each task in the registry can be driven independently through the loop, in the order the sequencing established. This is the single seam between planning and building: everything before it is conversation and documents, everything after it is the per-task loop.

## Guidelines

### Do

- Resolve the profile first and use the configured `artifact_root` and `task.id_scheme` everywhere.
- Build the plan on top of the architecture's settled decisions, not around them.
- Trace every task back to the requirement identifiers it serves.
- Keep tasks flat, coherent, and individually testable.
- Group spec documents by area of concern for readability.
- Assign task ids in one global sequence and make the spec documents agree with the registry.
- Name a concrete first deliverable: the thinnest end-to-end slice.
- Spawn the decomposers concurrently and wait for all of them before assembling the registry.

### Do not

- Introduce epics, stories, story points, or sprint ceremony. The unit is the flat task.
- Restart task numbering per area. The sequence is global.
- Reference any external tracker, the gh CLI, or a CI gate. The registry is the system of record.
- Reopen decisions already settled in the architecture or the requirements.
- Set any task to a status other than `planned`; no phase has run at planning time.
- Hardcode a project specific. All coupling is read from `sdlc.config.yaml`.

## Completion

Return a 3 line summary: the number of spec documents and the number of tasks in the registry; the first deliverable and the tasks it comprises; and a pointer to `implementation-plan.md` and `specs/index.md` as the handoff into `implement-task`.
