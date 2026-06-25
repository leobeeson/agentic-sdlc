# Reviews

This directory holds one subdirectory per task, `<task-id>/`, containing the review panel's output. Each reviewer in the configured roster writes one file named for its dimension (for example `correctness.md`). The `review-consolidator` then writes `consolidated.md`, the authoritative verdict.

Reviewers are read-only and adversarial. Each owns one dimension and hunts the whole codebase for where the change violates it. Code and deployed configuration are the only source of truth. No finding is asserted without a trace to the actual file and line.

## Per-dimension review format (`<dimension>.md`)

```
# Review: TASK-NNN, dimension <dimension>

## Findings
### <ID> <C|H|M|L> <short title>
- Severity: critical | high | medium | low (irreversibility x silence x blast-radius).
- Failure shape: what goes wrong.
- Evidence: file:line quotes proving it.
- Live on deploy? yes | dark (and the flag that gates it).
- Fix direction: the smallest correct change.

## Coverage ledger
- Invariant owned: the dimension's claim.
- Traced: the consumers and call sites checked.
- Swept: the full grep match set, each with a verdict.
- Not opened: what was out of scope and why.
```

## Consolidated review format (`consolidated.md`)

```
# Consolidated Review: TASK-NNN <name>

**Verdict:** safe to proceed | changes required | reconciliation needed
**Critical:** <count>  **High:** <count>

## Headline
One paragraph: the state of the change.

## Findings (deduplicated, severity ranked)
| ID | Severity | Dimension | Title | Evidence | Live? |
|----|----------|-----------|-------|----------|-------|

## Detail (high and above)
Per finding: the failure, the evidence re-validated against code, the fix direction.

## Disagreements resolved
Where reviewers conflicted, what the evidence showed, and the call made.

## Coverage
The combined coverage across reviewers, and anything left unopened.
```
