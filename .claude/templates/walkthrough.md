# Walkthroughs

This directory holds one walkthrough per task, `<task-id>.md`, produced by the `code-walkthrough`. A walkthrough is an execution-flow-ordered guided tour of the implemented code, so the developer can understand and audit it before merge. It orders stops by execution flow, not by file tree. Maximum 15 stops per task.

## Walkthrough format

```
# Walkthrough: TASK-NNN <name>

## Overview
Two or three sentences on what the change does.

## Reading order
A numbered list, in execution-flow order:
1. `path/to/file` : <function>, <one line>.

## Stops
For each stop:
- File: `path/to/file` lines X to Y.
- Requirement: the brief "Must" it satisfies.
- Description: what this code does.
- Pattern: the convention it follows (from the exploration or reference docs).
- Connects to: the next stop in the flow.
- Worth noticing: optional.

## Test map
| Stop | Test | What it verifies |
|------|------|------------------|

## Decisions made
| Decision | Rationale | Reference |
|----------|-----------|-----------|

## Questions to consider
Things the developer should confirm before merge.
```
