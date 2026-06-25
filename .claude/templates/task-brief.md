# Task briefs

This directory holds one brief per task, `<task-id>.md`, produced by the `task-preparer`. A brief is a focused, self-contained instruction set for implementing a single task. It distils the spec (what to build) and the exploration (current codebase state) into one document. Keep a brief under 150 lines.

## Task brief format

```
# Task Brief: TASK-NNN <name>

**Spec:** specs/NN-<area>.md (the TASK-NNN section)
**Exploration:** explorations/TASK-NNN.md
**Classification:** HITL (needs human decisions) | AFK (can run unattended)

## Objective
One sentence.

## Requirements
- Must: ...
- Should: ...
- Out of scope: ...

## Human checkpoints
Decisions that need a human (HITL). None for AFK.

## Test plan
- Behaviours to verify, prioritised.
- Testing approach, per the configured testing conventions.
- Interfaces to test through.

## Technical context
- What exists (from the exploration).
- What this task creates.

## Code hints
- Files likely involved.
- Patterns to follow.
- Patterns to avoid.

## Success criteria
The conditions under which this task is done.
```
