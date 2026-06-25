---
name: implement-task
description: The orchestration spine for implementing one flat task end to end. Use when starting a task from a spec, resuming a task partway through, or running just one phase (explore, prepare, implement, review panel, consolidate, walkthrough, or reconcile). The review panel and consolidator are also invocable standalone on any existing change. Each phase is independently callable and the loop resumes from whatever artifacts already exist.
---

# Implement Task

The orchestration spine for the implementation phase. It drives one flat task (for example `TASK-001`) through seven phases, in order: explore, prepare, implement, review panel, consolidate, walkthrough, and reconcile. The headless subagents live in `.claude/agents/`; this skill spawns them, owns the task registry, and never converses on their behalf.

Each phase is independently callable. The loop resumes from whatever artifacts already exist, so a session can pick up at any phase. The review panel plus consolidator can also be run standalone on an existing change, outside the loop entirely.

## What this skill reads from the profile

Everything project-specific is read at runtime from `sdlc.config.yaml` at the repository root. Resolve these before driving any phase:

- `artifact_root`, default `ai_docs`. All artifacts live under this tree. Prose below uses `ai_docs/`, but the value is always the configured root.
- `task.id_scheme`, for example `TASK-{NNN}`. The shape of a task id.
- `vcs.default_base_branch`, for example `master`. The `base_ref` passed to every reviewer.
- `test_gate.commands`, the test commands the developer runs during implementation.
- `review.roster`, the list of review dimensions.
- `review.mode`, either `thorough` (full roster) or `light` (a subset).

Resolve a task's spec document by looking it up in `<artifact_root>/specs/index.md`. The registry is the map from task id to spec document. Never hardcode a prefix-to-spec mapping.

## The artifact tree

All artifacts land under the configured `artifact_root`. This is the same tree the setup skill creates.

```
ai_docs/
  charter.md                      Phase 0 output
  prd.md                          Phase 1 output
  architecture.md                 Phase 2 output
  implementation-plan.md          Phase 3 output
  diagrams/                       Phase 2 diagrams
  specs/
    index.md                      Task registry: task to spec map and status board
    NN-<area>.md                  Per-area spec documents, contain tasks
  reference/                      Living project-state documents
    CONTEXT.md                    Domain glossary, ubiquitous language
    testing-conventions.md        Testing patterns and cadence
    adr/                          Architectural decision records
    <domain>.md                   One per concern, created as needed
  task-briefs/
    <task-id>.md                  Per-task brief (task-preparer)
  explorations/
    <task-id>.md                  Per-task exploration (feature-explorer)
  reviews/
    <task-id>/
      <dimension>.md              One per reviewer in the roster
      consolidated.md             The authoritative consolidated verdict
  walkthroughs/
    <task-id>.md                  Per-task walkthrough (code-walkthrough)
  reconciliations/
    <task-id>.md                  Per-task reconciliation (spec-reconciler)
  runbook.md                      How to run phases
```

## Phase map

| # | Phase | Agent | Input | Output |
|---|-------|-------|-------|--------|
| 1 | Explore | feature-explorer | Spec document + codebase + reference docs | `explorations/<task-id>.md` |
| 2 | Prepare | task-preparer | Spec + exploration + reference docs | `task-briefs/<task-id>.md` |
| 3 | Implement | the developer with Claude | Brief + exploration | Code + tests |
| 4 | Review panel | reviewer-<dimension> (one per dimension, in parallel) | Diff vs base ref + spec + code | `reviews/<task-id>/<dimension>.md` |
| 5 | Consolidate | review-consolidator | Every reviewer file for the task | `reviews/<task-id>/consolidated.md` |
| 6 | Walkthrough | code-walkthrough | Brief + exploration + consolidated review + code | `walkthroughs/<task-id>.md` |
| 7 | Reconcile | spec-reconciler | Consolidated review + spec | Updated spec in place + `reconciliations/<task-id>.md` |

## The orchestrator owns the registry

The agents never edit `<artifact_root>/specs/index.md`. This skill does. After each phase completes, update the task's row in the registry: advance the status and link the new artifact. Status values, in order:

- `planned`: the task exists in a spec but no phase has run.
- `in-progress`: explore, prepare, or implement has run; implementation is not yet reviewed.
- `implemented`: implementation is done and the review panel plus consolidator have run.
- `reviewed`: the walkthrough has run and the task is ready for reconciliation.
- `reconciled`: the spec has been reconciled to the built reality. The task is complete.

Update the registry as the final step of each phase, so the status board always reflects exactly what has been produced.

## Phase 1: Explore

Agent: `feature-explorer`, read-only.

Run the explorer in preparation mode. It reads the task's spec section (resolved through `specs/index.md`), `reference/CONTEXT.md`, `reference/testing-conventions.md`, the codebase, other repos on disk, and online docs, then writes the exploration report.

Invoke:

```
Run feature-explorer for TASK-001 in preparation mode at medium depth
```

Output: `<artifact_root>/explorations/<task-id>.md`.

Registry: set the task status to `in-progress` and link the exploration.

The explorer is also the side-quest agent during implementation. Any time you would otherwise read five or more files to answer a question, or research an unfamiliar library, delegate it:

```
Run feature-explorer to investigate <specific question>
```

In ad-hoc mode it returns findings directly and writes no report.

## Phase 2: Prepare

Agent: `task-preparer`.

The preparer reads the spec section, the exploration from phase 1, the reference docs, and any relevant ADRs. It writes a self-contained task brief: objective, requirements (must, should, out of scope), HITL checkpoints, a test plan with prioritised behaviours, technical context grounded in the exploration, code hints, and success criteria.

Invoke:

```
Run task-preparer for TASK-001
```

Output: `<artifact_root>/task-briefs/<task-id>.md`.

Registry: keep the task status at `in-progress` and link the brief.

Resume: if a brief already exists for the task, skip phases 1 and 2.

## Phase 3: Implement

No agent. The developer implements with Claude, using the brief and exploration as context.

Before writing code, read in this order:

1. The task brief at `<artifact_root>/task-briefs/<task-id>.md`.
2. The exploration at `<artifact_root>/explorations/<task-id>.md`.
3. `<artifact_root>/reference/CONTEXT.md` for domain vocabulary.
4. `<artifact_root>/reference/testing-conventions.md` for testing patterns and cadence.

Follow the test plan from the brief with TDD vertical slices, one behaviour at a time:

1. Write one test for the next behaviour (RED, it must fail).
2. Write minimal code to make it pass (GREEN, no more than needed).
3. Repeat for the next behaviour.
4. Refactor once all behaviours are green (REFACTOR).

Rules:

- Never write all tests first, then all code. Each test responds to what the previous cycle taught you.
- Never refactor while RED. Reach GREEN first.
- Tests verify behaviour through public interfaces, not implementation details.
- Mock only at system boundaries: model calls, database, external HTTP, time and randomness. Never mock internal classes you wrote.
- Test names describe what the system does, not how.

Run the test commands from `test_gate.commands` in the profile as the local gate during implementation.

At each HITL checkpoint in the brief, stop, present the decision with your recommendation, wait for the developer, record the outcome in `<artifact_root>/reference/adr/` if it meets the ADR bar (hard to reverse, surprising without context, the result of a real trade-off), then continue.

Registry: keep the task status at `in-progress` while implementation is underway.

## Phase 4: Review panel

Agents: the `reviewer-<dimension>` agents in `.claude/agents/reviewers/`, read-only, one per dimension.

Spawn one reviewer per dimension in `review.roster`, mapping each dimension to its `reviewer-<dimension>` agent under `.claude/agents/reviewers/`, all in parallel, in a single batch. Each reviewer obeys the no-assert-without-trace contract: code and deployed configuration are the only source of truth, the diff is the trigger and prime suspect but never the search boundary, and no finding is asserted without a trace to the actual file and line. Each reviewer receives the `task_id` and `base_ref` resolved from `vcs.default_base_branch`.

Honour `review.mode`:

- `thorough`: spawn the full roster.
- `light`: spawn the configured subset.

Invoke (one line per dimension, all spawned concurrently):

```
Run reviewer-spec-conformance for TASK-001, base_ref master
Run reviewer-correctness for TASK-001, base_ref master
Run reviewer-state-and-concurrency for TASK-001, base_ref master
Run reviewer-security-and-trust-boundary for TASK-001, base_ref master
Run reviewer-failure-and-robustness for TASK-001, base_ref master
Run reviewer-observability for TASK-001, base_ref master
Run reviewer-test-adequacy for TASK-001, base_ref master
Run reviewer-interface-and-data-integrity for TASK-001, base_ref master
Run reviewer-conventions for TASK-001, base_ref master
```

The reviewers run concurrently. Each writes its own file at `<artifact_root>/reviews/<task-id>/<dimension>.md`, giving full visibility into the raw findings before they are merged.

Wait for every reviewer to complete before phase 5. The consolidator runs only after the whole panel has finished.

Registry: do not advance the status yet; advance to `implemented` only after phase 5 completes.

## Phase 5: Consolidate

Agent: `review-consolidator`.

Run the consolidator only after all reviewers from phase 4 have completed. It reads every reviewer file under `reviews/<task-id>/`, deduplicates overlapping findings, resolves disagreements between reviewers, re-validates each surviving finding against the actual code to kill false positives, ranks by severity (irreversibility times silence times blast radius), and writes the authoritative verdict.

Invoke:

```
Run review-consolidator for TASK-001
```

Output: `<artifact_root>/reviews/<task-id>/consolidated.md`, ending in a verdict.

Registry: set the task status to `implemented` and link the consolidated review.

## Standalone review

The review panel and the consolidator are not only inner phases. They can be run on their own against any existing change, with no brief or exploration required. To review a branch or a working change directly:

1. Spawn the reviewer panel as in phase 4, passing the `task_id` (or a label for the change) and the `base_ref` to diff against, honouring `review.mode`.
2. After the panel finishes, run `review-consolidator` for the same identifier.

The outputs land in the same `reviews/<task-id>/` location. Update the registry only if the change corresponds to a registered task.

## Phase 6: Walkthrough

Agent: `code-walkthrough`.

The walkthrough agent reads the task brief, the exploration, the consolidated review, the reference docs, and every implementation file. It traces the execution flow and writes an execution-flow-ordered walkthrough, with ordered stops linked back to brief requirements and exploration patterns, for the developer to audit the code before merge.

Invoke:

```
Run code-walkthrough for TASK-001
```

Output: `<artifact_root>/walkthroughs/<task-id>.md`.

Registry: set the task status to `reviewed` and link the walkthrough.

## Phase 7: Reconcile

Agent: `spec-reconciler`.

The reconciler reads the consolidated review and the spec, taking the implementation as ground truth. It updates the spec document in place so it reflects what was actually built, updates `reference/` and `reference/adr/` as needed, and writes the reconciliation report as the audit trail of what changed and why.

Invoke:

```
Run spec-reconciler for TASK-001
```

Output: the updated spec document (mutated in place) and `<artifact_root>/reconciliations/<task-id>.md`.

Registry: set the task status to `reconciled` and link the reconciliation. The task is now complete.

## Resume behaviour

The loop is resumable from any phase. To resume a task, read the artifacts already present under `<artifact_root>` and the task's row in `specs/index.md`, then continue from the first phase whose output is missing:

- Exploration present, brief absent: resume at phase 2.
- Brief present, no implementation: resume at phase 3.
- Implementation present, no reviewer files: resume at phase 4.
- Reviewer files present, no consolidated review: resume at phase 5.
- Consolidated review present, no walkthrough: resume at phase 6.
- Walkthrough present, no reconciliation: resume at phase 7.

Trust the artifacts and the registry status as the record of progress. Do not re-run a phase whose output already exists unless the developer asks for it.

## Completion

When the loop finishes, return a 3 line summary: the task id and its final registry status, the phases run and any skipped, and the consolidated verdict with a pointer to the artifacts.
