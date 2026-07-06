<!-- TEMPLATE: the exploration report for one task. Owner: the feature-explorer
     subagent (preparation mode; ad-hoc mode returns findings directly and
     writes no file). Path:
     ai_docs/initiatives/<initiative-id>/explorations/<task-id>.md. An
     exploration is an evidence-only report of the current codebase state
     relevant to a task: file paths, line numbers, signatures, snippets, and
     integration points. It never speculates and never proposes a design. -->

<!-- PROVENANCE (append-only; only created is fixed) -->
created:        <ISO-8601 timestamp>
modified:       [<ISO-8601 timestamp>]
commits:        [<short-sha>]
agents:         [feature-explorer]
run-ids:        [<run-id>]
back-refs:      [specs/<spec-file>.md, reference/CONTEXT.md]
forward-refs:   [task-briefs/<task-id>.md]
<!-- END PROVENANCE -->

# Exploration: <task-id> <task name>

**Depth:** quick | medium | thorough
**Scope:** <what was investigated>

## Summary

<A few sentences: what exists in the codebase relevant to this task, what does not exist yet, and the key findings that will affect implementation or review.>

## Files analysed

| File | Purpose | How the task interacts with it |
| --- | --- | --- |
| <path> | <what it does> | <create / modify / integrate / read> |

## Code structure

<Per relevant file: key signatures, short snippets (10 to 15 lines) when the pattern needs to be visible, and the exact integration points where new or changed code connects.>

## Existing test patterns

<How the relevant area is tested today: organisation, naming, fixtures, what is mocked against what is real, coverage gaps relevant to this task.>

## External research (if applicable)

<Documentation or references consulted, with URLs.>

## Patterns to follow

<Conventions already in the codebase that this task should match, one concrete example per pattern with its path.>

## Patterns to avoid

<Anti-patterns observed that this task should not repeat, and what to do instead.>

## Complications

| Concern | Location | Impact | Suggestion |
| --- | --- | --- | --- |
| <issue> | <file:line> | <what could go wrong> | <how to mitigate> |

## Unanswered questions

<What could not be determined from the code, and the ambiguities that became apparent during exploration.>
