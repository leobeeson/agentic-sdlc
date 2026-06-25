# Task Registry

The single source of truth for every task: its spec document, its status, and the artifacts produced for it. This registry replaces any external tracker. The `plan-implementation` skill creates entries; the implementation-phase agents update status and artifact links as work proceeds.

Status values: planned, in-progress, implemented, reviewed, reconciled.

| Task | Spec | Name | Status | Brief | Exploration | Review | Walkthrough | Reconciliation |
|------|------|------|--------|-------|-------------|--------|-------------|----------------|
| TASK-001 | 00-<area> | <name> | planned | - | - | - | - | - |

## How to read this

- Spec: the spec document under `specs/` that defines the task.
- Brief, Exploration, Review, Walkthrough, Reconciliation: a link to the artifact once produced, or `-` if not yet produced.
- A task is reconciled when its spec document has been updated to reflect what was actually built.
