# Reconciliations

This directory holds one reconciliation per task, `<task-id>.md`, produced by the `spec-reconciler`. It takes the implementation as ground truth, updates the spec document in place so it reflects what was actually built, updates the reference docs, and records here every change made and why. There is no external tracker to sync; this report and the updated spec are the record.

## Reconciliation format

```
# Reconciliation: TASK-NNN <name>

## Summary
What deviated from the spec and what was updated.

## Deviations
| Type | Spec said | Implementation does | Rationale |
|------|-----------|---------------------|-----------|

Type is one of: implementation_detail, interface_change, behaviour_change, scope_change.

## Spec updates applied
The exact edits made to specs/NN-<area>.md, quoted before and after, with the files that implement each.

## Downstream impact
| Future task | Severity | What changed | Recommendation |
|-------------|----------|--------------|----------------|

Severity is one of: blocking, requires_adjustment, informational.

## Reference docs updated
| Document | Change |
|----------|--------|

## Decision records
| Record | Why it was created |
|--------|--------------------|
```
