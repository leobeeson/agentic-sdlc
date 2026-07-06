<!-- TEMPLATE: the task registry for one initiative. Owner: the
     implementation-planner skill, which writes it as part of decomposition;
     when the planner is not in the composed plan, the orchestrator itself
     records the single minted task here (a bookkeeping write, like the run
     record). Path: ai_docs/initiatives/<initiative-id>/specs/index.md. The
     registry is the map from task identifier to its spec document, plus the
     status board the orchestrator and the reconciler keep current. Artefacts
     are addressed by the composite join key <initiative-id>/TASK-XXX, so every
     path below is deterministic. -->

<!-- PROVENANCE (append-only; only created is fixed) -->
created:        <ISO-8601 timestamp>
modified:       [<ISO-8601 timestamp>]
commits:        [<short-sha>]
agents:         [implementation-planner]
run-ids:        [<run-id>]
back-refs:      [implementation-plan.md]
forward-refs:   [specs/<spec-file>.md]
<!-- END PROVENANCE -->

# Task Registry: <initiative-id>

Status values: planned, in-progress, implemented, reviewed, reconciled.

| Task | Spec | Name | Status | Brief | Exploration | Review | Walkthrough | Reconciliation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TASK-001 | specs/NN-<area>.md | <name> | planned | - | - | - | - | - |

## How to read this registry

- Spec: the spec document under `specs/` that defines the task.
- Brief, Exploration, Review, Walkthrough, Reconciliation: a link to the artefact once produced, or `-` when not yet produced.
- A task is reconciled when the reconciler has confirmed the recorded plan agrees with what was actually built.
