<!-- TEMPLATE: the task brief, the distilled, self-contained work order the
     implementation consumes. Owner: the task-preparer subagent. Path:
     ai_docs/initiatives/<initiative-id>/task-briefs/<task-id>.md. The brief
     distils the spec (what to build) and the exploration report (current
     codebase state) into one document a fresh session can implement from.
     Keep a brief under 150 lines. The Degraded inputs section appears only
     when an optional input was absent; it sits directly after the provenance
     header so the template's structure is untouched. -->

<!-- PROVENANCE (append-only; only created is fixed) -->
created:        <ISO-8601 timestamp>
modified:       [<ISO-8601 timestamp>]
commits:        [<short-sha>]
agents:         [task-preparer]
run-ids:        [<run-id>]
back-refs:      [specs/<spec-file>.md, explorations/<task-id>.md, reference/CONTEXT.md]
forward-refs:   [<the generated product>, reviews/<task-id>/]
<!-- END PROVENANCE -->

## Degraded inputs

<Present only when an optional input was absent. One line per absent input, for example:>
- exploration_report: absent. This brief was prepared from the spec and the reference documents only.

# Task Brief: <task-id> <task name>

**Spec:** specs/<spec-file>.md (the <task-id> section)
**Exploration:** explorations/<task-id>.md
**Classification:** HITL (needs human decisions) | AFK (can run unattended)

## Objective

<What this task delivers. One to three sentences.>

## Requirements

- Must: <concrete, verifiable requirements, each mapping to a testable behaviour>
- Should: <non-critical but expected behaviour>
- Out of scope: <what this task does not do, naming the task that handles each deferred item>

## Human checkpoints

<Decisions requiring human input before proceeding, each with context and a recommendation. "No checkpoints; this task can proceed autonomously." when none.>

## Test plan

- Behaviours to verify, prioritised.
- Testing approach, per reference/testing-conventions.md: what to mock (only system boundaries), the real defaults used in place of mocks.
- Interfaces to test through, grounded in the exploration report's existing test patterns.

## Technical context

- What exists: key files, integration points, and patterns, grounded in the exploration report.
- What this task creates: new files, classes, functions, endpoints, and any pattern later tasks will follow.

## Code hints

- Files likely involved, each with its role.
- Patterns to follow, with where each exists in the codebase.
- Patterns to avoid, with what to do instead.

## Success criteria

<The conditions under which this task is done: every Must verified by a test, the validation commands pass, no regressions, the vocabulary of reference/CONTEXT.md used throughout.>
