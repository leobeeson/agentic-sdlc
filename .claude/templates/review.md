<!-- TEMPLATE: one per-dimension review. Owner: the reviewer subagent that owns
     the dimension (one file per reviewer in the selected subset). Path:
     ai_docs/initiatives/<initiative-id>/reviews/<task-id>/<dimension>.md. The
     review-consolidator reads every file in reviews/<task-id>/ and writes
     consolidated.md (see consolidated-review.md). Reviewers are read-only over
     the code and adversarial: each owns one dimension and hunts for where the
     change violates it. Code and deployed configuration are the only source of
     truth. No finding is asserted without a trace to the actual file and line.
     The status field is always present: failure is part of the type, not a
     missing file. -->

<!-- PROVENANCE (append-only; only created is fixed) -->
created:        <ISO-8601 timestamp>
modified:       [<ISO-8601 timestamp>]
commits:        [<short-sha>]
agents:         [reviewer-<dimension>]
run-ids:        [<run-id>]
back-refs:      [<the diff or change reviewed>, specs/<spec-file>.md]
forward-refs:   [reviews/<task-id>/consolidated.md]
<!-- END PROVENANCE -->

# Review: <task-id>, dimension <dimension>

**Status:** complete | failed
**Safe to proceed (this dimension):** yes | no | after_fixes
**Summary:** <two to four sentences: what was built, judged against the spec.>

## Findings

### <number>. <short title>

- Severity: blocker | should_fix | nice_to_have
- Description: <what goes wrong, the failure shape.>
- Evidence: <file:line, with the quoted lines proving it. No finding without a trace.>
- Resolution: <the concrete, smallest correct fix the reviewer proposes.>
- Live on deploy: yes | dark (<and the flag that gates it>)

## Escalations

<Questions with material impact on the intent that this reviewer did not settle by assumption. "None" when none.>

## Risks

<Inconsistencies and risks the next stages build on. "None" when none.>

## Coverage ledger

- Invariant owned: <the dimension's claim over the change.>
- Traced: <the consumers and call sites checked.>
- Swept: <the full grep match set, each with a verdict.>
- Not opened: <what was out of scope and why.>
