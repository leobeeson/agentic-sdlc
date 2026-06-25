# Explorations

This directory holds one exploration per task, `<task-id>.md`, produced by the `feature-explorer`. An exploration is an evidence-only report of the current codebase state relevant to a task: file paths, line numbers, signatures, snippets, and integration points. It never speculates and never proposes a design.

## Exploration format

```
# Exploration: TASK-NNN <name>

**Depth:** quick | medium | thorough
**Scope:** what was investigated.

## Summary
A few sentences of findings.

## Files analysed
| File | Purpose | How the task interacts with it |
|------|---------|--------------------------------|

## Code structure
Per file: key signatures, short snippets (10 to 15 lines), and integration points.

## Existing test patterns
How the relevant area is tested today.

## External research (if applicable)
Documentation or references consulted, with URLs.

## Patterns to follow
Conventions already in the codebase that this task should match.

## Patterns to avoid
Anti-patterns observed that this task should not repeat.

## Complications
| Concern | Location | Impact | Suggestion |
|---------|----------|--------|------------|

## Unanswered questions
What could not be determined from the code.
```
