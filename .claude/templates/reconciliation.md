<!-- TEMPLATE: the reconciliation record for one task. Owner: the reconciler
     subagent, triggered by the orchestrator at each task boundary. Path:
     ai_docs/initiatives/<initiative-id>/reconciliations/<task-id>.md. The code
     is the ground truth. The write boundary is drawn by ownership: an
     agent-authored, regenerable artefact (the forward entries of the
     implementation plan, an unconsumed task brief) is overwritten in place; a
     human-gated artefact (the PRD, an ADR, an approved spec) receives a
     proposed edit here, never an overwrite; code is never touched; and the
     living reference documents have one writer, the context-agent, so
     vocabulary drift is flagged here for the orchestrator to chain a
     context-agent refresh. The reconciler is a no-op when the task had no
     downstream impact, and a valid no-op still writes this record with the
     no-op stated. -->

<!-- PROVENANCE (append-only; only created is fixed) -->
created:        <ISO-8601 timestamp>
modified:       [<ISO-8601 timestamp>]
commits:        [<short-sha>]
agents:         [reconciler]
run-ids:        [<run-id>]
back-refs:      [<the task's implemented change>, implementation-plan.md, specs/index.md]
forward-refs:   [<the artefacts updated or flagged>]
<!-- END PROVENANCE -->

# Reconciliation: <task-id> <task name>

## Summary

<What deviated from the recorded plan, and the scope of downstream impact. "No downstream impact; no reconciliation action taken." for a no-op.>

## Deviations

| Type | Recorded plan said | Implementation does | Rationale |
| --- | --- | --- | --- |
| <implementation_detail / interface_change / behaviour_change / scope_change> | <quote> | <reality> | <from commits or code, or "not documented"> |

## Artefacts overwritten in place

Agent-authored, regenerable artefacts only: the forward entries of the implementation plan, unconsumed task briefs.

| Artefact | Change |
| --- | --- |
| <path> | <what was updated and why a stale version had no value> |

## Proposed edits to human-gated artefacts

Never applied directly: the PRD, ADRs, and approved specs record decisions a person approved, so each edit below lands only with the developer's approval.

### <artefact and section>

**Current:**
> <quote>

**Proposed:**
> <clean replacement text>

**Implemented by:** `<paths>`

## Vocabulary drift flagged

The living reference documents (CONTEXT.md, the ubiquitous language, the testing conventions) have one writer, the context-agent. Drift detected here is flagged, not written; the orchestrator chains a context-agent refresh at this task boundary.

- <term or convention that drifted, and the evidence. "None" when none.>

## Downstream impact

| Future task | Severity | What changed | Recommendation |
| --- | --- | --- | --- |
| <task-id> | blocking / requires_adjustment / informational | <impact> | <action> |

Code is never touched by reconciliation: the code is the ground truth the reconciliation reads, never a surface it writes.
