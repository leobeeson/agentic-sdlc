# Phase 4: Implement Task

## Purpose

Phase 4 implements one flat task end to end. It drives a single task, for example `TASK-001`, through seven stages in order: explore, prepare, implement, review panel, consolidate, walkthrough, and reconcile. Each stage produces an evidence artifact, and the orchestrator advances the task's status in the registry as each completes. This is the back half of the pipeline and it is headless: an orchestration skill drives subagents that run in fresh context, report evidence, and never converse on the developer's behalf.

Each stage is independently callable, and the loop resumes from whatever artifacts already exist, so a session can pick up at any stage. The review panel and the consolidator can also be run standalone on any existing change, outside the loop entirely.

## Inputs

- `sdlc.config.yaml`, resolved first, for `artifact_root` (default `ai_docs`), `task.id_scheme`, `vcs.default_base_branch` (the `base_ref` passed to every reviewer), `test_gate.commands` (the local gate during implementation), `review.roster` (the review dimensions), and `review.mode` (`thorough` for the full roster, `light` for a subset).
- `<artifact_root>/specs/index.md`, the task registry, to resolve a task's spec document. The registry is the map from task id to spec document; the orchestrator never hardcodes a prefix-to-spec mapping.
- The task's spec document under `<artifact_root>/specs/`, the reference docs (`reference/CONTEXT.md`, `reference/testing-conventions.md`, and any relevant ADRs), the codebase, and, per stage, the artifacts produced by earlier stages of the same task.

## What it produces

Per task, under the configured `artifact_root` (default `ai_docs`):

- `explorations/<task-id>.md`, the exploration report (feature-explorer).
- `task-briefs/<task-id>.md`, the task brief (task-preparer).
- The code and tests for the task (the developer with Claude).
- `reviews/<task-id>/<dimension>.md`, one file per reviewer in the roster (code-reviewer).
- `reviews/<task-id>/consolidated.md`, the authoritative consolidated verdict (review-consolidator).
- `walkthroughs/<task-id>.md`, the execution-flow-ordered walkthrough (code-walkthrough).
- The spec document updated in place to match what was built, and `reconciliations/<task-id>.md`, the audit trail of what changed and why (spec-reconciler).

The orchestrator also updates the task's row in `specs/index.md` after each stage: it advances the status through `planned`, `in-progress`, `implemented`, `reviewed`, `reconciled`, and links the new artifact. The agents never edit the registry; the orchestrator owns it.

## How to run

- Command: `/implement-task <task-id>` for the full loop, or `/review <task-id>` for the standalone review path.
- Skill: `implement-task`.
- Agents spawned, in order:
  - `feature-explorer`, read-only. Runs in preparation mode and writes the exploration report. It is also the side-quest agent during implementation: any investigation that would otherwise read five or more files is delegated to it in ad-hoc mode, where it returns findings directly and writes no report.
  - `task-preparer`. Reads the spec, the exploration, and the reference docs, and writes the self-contained task brief, classifying the task HITL or AFK.
  - The implement stage has no agent. The developer implements with Claude, reading the brief, the exploration, and the reference docs, following the test plan with TDD vertical slices (one failing test, minimal code to pass, repeat, then refactor), running `test_gate.commands` as the local gate, and stopping at each HITL checkpoint in the brief.
  - `code-reviewer`, read-only, spawned once per dimension in `review.roster`, all in parallel in a single batch, honouring `review.mode`. Each reviewer owns one dimension, treats code and deployed configuration as the only source of truth, takes the diff as the trigger and prime suspect but never the search boundary, asserts no finding as live or as Critical or High without a trace to the actual `file:line`, and writes its own dimension file. The orchestrator waits for the whole panel before consolidating.
  - `review-consolidator`. Runs only after the whole panel finishes. It reads every reviewer file, deduplicates overlapping findings, resolves disagreements, re-validates each surviving finding against the actual code to kill false positives, ranks by severity (irreversibility times silence times blast radius), and writes the consolidated verdict, which is `safe to proceed`, `changes required`, or `reconciliation needed`.
  - `code-walkthrough`. Reads the brief, the exploration, the consolidated review, the reference docs, and every implementation file, traces the execution flow, and writes the walkthrough ordered by how the code runs, each stop linked to a brief requirement.
  - `spec-reconciler`. Takes the implementation as ground truth. It updates the spec document in place to reflect what was built, updates the context doc and reference docs, records any qualifying decision, and writes the reconciliation report as the audit trail.

The standalone review path spawns the `code-reviewer` panel and then the `review-consolidator` for any existing change, with no brief or exploration required. The outputs land in the same `reviews/<task-id>/` location, and the registry is updated only if the change corresponds to a registered task.

The loop is resumable: the orchestrator reads the artifacts already present and the registry status, then continues from the first stage whose output is missing, and does not re-run a stage whose output already exists unless the developer asks.

## What good output looks like

- The status board in the registry reflects exactly what has been produced, advanced as the final step of each stage.
- The exploration cites exact file paths and line numbers, reports only what it found, and proposes no design.
- The brief is self-contained: a fresh session can implement the task from the brief alone, supplemented by the exploration. It is under 150 lines, distils the spec rather than copying it, and raises a HITL checkpoint only for a real open ambiguity, not for a decision already settled in an ADR.
- The implementation followed TDD vertical slices, mocked only at system boundaries, and the test gate passes.
- Each reviewer file carries findings only, ends with a mandatory coverage ledger, and asserts no live or high-severity finding without a trace. A dimension that holds says so plainly and says what was checked.
- The consolidated verdict carries no finding the consolidator did not re-validate against the code, ranks the most damaging failure first rather than the most visible, records every resolved disagreement and every dropped false positive, and reaches a clear top-line verdict.
- The walkthrough is ordered by execution flow rather than file tree, links every stop to a must requirement, explains design choices rather than narrating lines, and includes the test map.
- The reconciliation takes the implementation as ground truth, applies the spec edits in place as clean spec language, quotes the before and after of each edit, analyses downstream impact even for minor deviations, and never invents rationale.

## Hand-off

Phase 4 is the last phase and the end of the pipeline for a task. Within the loop, each stage hands its artifact to the next, and the orchestrator's registry status is the record of progress. When the loop finishes, the task's status is `reconciled` and the task is complete. The spec document, reconciled to the built reality, and the updated reference docs and glossary become the standing context that the next task's exploration and preparation read, so each completed task improves the ground every following task is built on. There is no separate phase beyond this: the adversarial review method lives inside the review panel, and the registry remains the single system of record.
