<!-- TEMPLATE: the walkthrough for one task. Owner: the code-walkthrough
     subagent. Path:
     ai_docs/initiatives/<initiative-id>/walkthroughs/<task-id>.md. A
     walkthrough is an execution-flow-ordered guided tour of the implemented
     change, so the developer can understand and audit it before merge and
     carry the understanding forward into the next review, the next incident,
     and the next design decision. Stops are ordered by execution flow, never
     by file tree. Maximum 15 stops per task. -->

<!-- PROVENANCE (append-only; only created is fixed) -->
created:        <ISO-8601 timestamp>
modified:       [<ISO-8601 timestamp>]
commits:        [<short-sha>]
agents:         [code-walkthrough]
run-ids:        [<run-id>]
back-refs:      [<the diff or change>, reviews/<task-id>/, specs/<spec-file>.md]
forward-refs:   [none]
<!-- END PROVENANCE -->

# Walkthrough: <task-id> <task name>

## Overview

<Two or three sentences: what was built, how many files, and the high-level execution flow in one sentence.>

## Reading order

A numbered list, in execution-flow order:

1. `<path>` : <function or section>, <one line>.

## Stops

### Stop 1: <title>

- File: `<path>` lines X to Y.
- Requirement: <the brief "Must" or spec criterion it satisfies.>
- Description: <what this code does and why, two to four sentences; the design choice, not the syntax.>
- Pattern: <the convention it follows, from the exploration report or reference docs.>
- Connects to: <the stops this calls or is called by, forming the execution chain.>
- Worth noticing: <anything non-obvious; omit when nothing is surprising.>

## Test map

| Stop | Test | What it verifies |
| --- | --- | --- |
| 1 | `<test file>::<test name>` | <behaviour verified> |

## Decisions made

| Decision | Rationale | Reference |
| --- | --- | --- |
| <what was decided> | <why> | <ADR / task brief / exploration report> |

## Questions to consider

<Things the developer should confirm before merge, and points worth carrying into future tasks.>
