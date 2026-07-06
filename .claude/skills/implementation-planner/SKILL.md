---
name: implementation-planner
description: |
  Produces the implementation plan, the per-task spec documents, and the task registry, in the
  initiative workspace. Load after the architecture and PRD exist, when the work decomposes
  into more than one task or needs an ordered, tracked breakdown. A gated consultation:
  explore, confirm, generate, refine. Spawns feature-explorer subagents to investigate the
  decomposition without flooding the conversation.
allowed-tools: Read, Grep, Glob, Bash, Write
model: opus
inputs:
  - name: architecture
    required: true
    signal: the settled design and its decisions that the plan decomposes into tasks
    source: ai_docs/architecture.md and reference/adrs/, written by the arch-blueprint agent
  - name: prd
    required: true
    signal: the requirements and acceptance criteria each task and spec must trace back to
    source: ai_docs/prd.md, written by the requirements-navigator agent
outputs:
  - type: implementation plan
    location: ai_docs/initiatives/<initiative-id>/implementation-plan.md (the initiative workspace)
  - type: per-task spec documents
    location: ai_docs/initiatives/<initiative-id>/specs/ (one spec per task, named by the task identifier)
  - type: task registry
    location: ai_docs/initiatives/<initiative-id>/specs/index.md
preconditions: a valid architecture and a valid PRD must both be present
intents:
  - ad-hoc code development (new feature and above magnitudes)
  - ADP Foundry YAML generation (new feature and above magnitudes)
  - dbt-model generation (new feature and above magnitudes)
scope: core
model_floor: strong
cost_tier: heavy
standalone: partial
idempotency: reuse an existing valid implementation-plan.md, its specs, and the task registry rather than regenerating them
primitive: skill
phase: phase-1
---

# Implementation Planner

The decomposition consultation, and the join between the specification stages and the generation loop. It turns the settled architecture and requirements into three artefacts in the initiative workspace: the implementation plan (the narrative), the per-task specs (the self-contained work orders the generation stage executes), and the task registry (the map and status board). Two agent roles write specification at two altitudes: this one decomposes an initiative into tasks; the task-preparer later turns one task into an executable work order. A wrong decomposition misdirects every task downstream, which is why this agent role runs on the strong tier.

This is a gated consultation performed by the main agent in the conversation: explore, confirm, generate, refine.

## Idempotency, checked first

Check the initiative workspace `ai_docs/initiatives/<initiative-id>/` before anything else.

- The plan, specs, and registry exist and validate against their templates: reuse them and move to refinement mode. Refinement adjusts affected tasks in place and appends new tasks to the registry; it never renumbers existing task identifiers.
- The artefacts are absent: run the consultation.

The initiative identifier is minted by the orchestrator at composition and supplied to this stage; every artefact this stage writes is addressed by the join key `<initiative-id>/TASK-NNN`.

## Resolve the inputs

Both inputs are required; this agent role is only partially standalone because decomposition without a settled design and traceable requirements produces guesswork.

- Read `ai_docs/architecture.md` and the ADRs in full: the components, boundaries, data flows, and settled decisions are what the plan decomposes. Never reopen a settled decision here; when one looks wrong, raise it.
- Read `ai_docs/prd.md` in full: every task must trace to the REQ and NFR identifiers it serves.
- Read `sdlc.config.yaml` for `validation.commands` (each spec's Validation Commands section draws from these), `product_locations` (where each task's product lands), and the stack.
- Read `ai_docs/reference/CONTEXT.md` and `ai_docs/reference/testing-conventions.md` when present, and use their vocabulary and conventions in every spec.

## The consultation

Explore the topics below with the developer. Hold the mental graph; regularly zoom out to check the emerging plan still serves the charter's objectives and the PRD's priorities.

- **Work breakdown.** The concrete units of work the architecture implies. Drive towards flat tasks, each a coherent vertical slice: independently implementable, independently verifiable, delivering an observable increment. No epics, no stories, no sprints; the unit is the task.
- **Sequencing and dependencies.** The order the architecture forces: producers before consumers (a source definition before the model that reads it; an ingestion DAG before the transformation trigger that depends on its output). Name each dependency explicitly.
- **The first deliverable.** The thinnest end-to-end slice that demonstrates the system working, and the tasks composing it. This anchors the sequence; there is no sprint ceremony to replace it.
- **Per-task validation.** How each task proves itself done: which of the profile's validation commands apply, with which selectors or arguments, and what evidence of zero regressions looks like.
- **Testing strategy.** The levels of testing across the initiative, consistent with the recorded testing conventions.
- **Risks.** What could go wrong, the tasks each risk lands on, and the mitigation, including schedule risks from external dependencies such as access routes.

Settle immaterial points by inference; ask when open readings would produce materially different plans.

## Fan-out: feature-explorer only

Spawn feature-explorer subagents, one per decomposition question, in a single message, when the breakdown needs evidence: which existing files a candidate task touches, whether two candidate tasks collide on the same surface, what an existing pipeline already provides. Fold the evidence back into the consultation. All investigation fan-out is the feature-explorer; the catalogue stays closed.

## The confirmation gate

Withhold the artefacts until every topic is explored and the developer explicitly confirms. Before asking, state: the candidate task list with one line each, the dependency order, the first deliverable, and the requirement coverage (every must-have REQ served by at least one task; every task tracing to at least one REQ or a recorded assumption), flagging every gap.

## Generate the three artefacts

Write, in the initiative workspace, filling each template's provenance header:

1. **The implementation plan** at `implementation-plan.md`, matching `.claude/templates/implementation-plan.md`: approach, work breakdown, sequencing and dependencies, first deliverable, testing strategy, risks. The plan is the narrative; the machine-readable handoff is the specs and the registry.
2. **One spec per task** under `specs/`, matching `.claude/templates/spec.md`. Each spec is a self-contained work order: task description; relevant files (with new files under a New Files heading); step-by-step tasks executed in order, the last step running the Validation Commands; Validation Commands that must run without errors, drawn from `validation.commands` with the task's own selectors; and notes. The spec is at once a durable artefact and the prompt the generation stage executes, so write each spec to be executable by a fresh agent with no other context.
3. **The task registry** at `specs/index.md`, matching `.claude/templates/specs-index.md`: one row per task, `TASK-001` onwards in one sequence per initiative, ordered to respect the dependencies, each row naming its spec, its serving requirement identifiers, and status `planned`.

Assign task identifiers yourself, in one pass, after the set is settled, so specs and registry agree on every identifier.

## Refinement mode

Subsequent turns adjust specific tasks, resequence, or append tasks in place. Never regenerate the set, and never renumber existing identifiers: the identifiers are the join key every downstream artefact is addressed by. The reconciler owns forward-plan corrections after tasks complete; this skill owns the plan until the first task starts.

## Guidelines

### Do

- Check idempotency first; refine an existing plan rather than regenerating it.
- Keep every task a self-contained vertical slice with its own validation commands.
- Sequence producers before consumers, and name the dependencies.
- Trace coverage both ways between requirements and tasks, and flag every gap.
- Write each spec as an executable work order for a fresh agent with no other context.

### Do not

- Generate before the double gate passes.
- Introduce epics, stories, points, or sprint ceremony.
- Renumber task identifiers once assigned.
- Reopen settled architecture or requirements; raise what looks wrong instead.
- Write implementation instructions beyond what the spec's steps need; the how belongs to the task-preparer and the generation stage.

## Handoff

The per-task loop consumes the registry in order: the feature-explorer and the task-preparer prepare each task, the generation stage executes its spec, and the downstream stages verify. The orchestrator drives the loop; in a hand-driven session the developer works the registry row by row.
