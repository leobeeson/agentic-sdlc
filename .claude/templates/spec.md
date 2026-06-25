# Spec documents

This directory holds spec documents, one per area of concern, named `NN-<area>.md` (for example `00-ingestion.md`). Spec documents group tasks for readability. The grouping is file organisation only, not a hierarchy level. The unit of work is the flat task.

Spec documents are living documents. After a task is implemented and reviewed, the `spec-reconciler` updates the spec in place so it always reflects the reality of what was built, not just what was originally intended. The task registry is `index.md`.

## Spec document format

```
# Spec NN: <Area>

## Overview
What this area of the system does and why it exists.

## Context
Constraints, prior decisions, and the requirement identifiers (REQ-00X) this area serves.

## Tasks

### TASK-NNN: <short name>
- Status: planned | in-progress | implemented | reconciled
- Objective: one sentence on what this task delivers.
- Requirements:
  - Must: ...
  - Should: ...
  - Out of scope: ...
- Acceptance criteria:
  - Given <state>, when <action>, then <observable result>.
- Dependencies: TASK-NNN (or none).
- Notes: reconciliation updates land here so the task reflects what was built.
```
