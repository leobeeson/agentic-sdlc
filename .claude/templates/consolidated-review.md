<!-- TEMPLATE: the consolidated review, the authoritative safe-to-proceed
     verdict. Owner: the review-consolidator subagent. Path:
     ai_docs/initiatives/<initiative-id>/reviews/<task-id>/consolidated.md.
     The consolidation is work, not collation: findings raised by several
     reviewers are de-duplicated, every finding is re-validated against the
     code and dropped when it does not reproduce, the survivors are ranked by
     severity, and the verdict block below is what the gate acts on. The gate
     blocks on blockers only: a gate that blocks on trivia trains the developer
     to override the gate. -->

<!-- PROVENANCE (append-only; only created is fixed) -->
created:        <ISO-8601 timestamp>
modified:       [<ISO-8601 timestamp>]
commits:        [<short-sha>]
agents:         [review-consolidator]
run-ids:        [<run-id>]
back-refs:      [reviews/<task-id>/<dimension>.md, <the diff or change reviewed>]
forward-refs:   [walkthroughs/<task-id>.md, reconciliations/<task-id>.md]
<!-- END PROVENANCE -->

# Consolidated Review: <task-id> <task name>

## Verdict

- Status: complete | failed
- Safe to proceed: yes | no | after_fixes
- Findings: <count raised by the panel>, <count confirmed against the code>
- Blockers: <count>
- Reconciliation needed: yes | no

## Headline

<One paragraph: the state of the change.>

## Findings (de-duplicated, re-validated, severity ranked)

| # | Severity | Dimension | Title | Evidence | Reproduce |
| --- | --- | --- | --- | --- | --- |
| 1 | blocker | <dimension> | <title> | <file:line> | `<execution command>` |

For a data-engineering artefact every finding carries a reproduce handle: the
execution command that shows the issue (for example `dbt build --select <model>`)
and the verification command that proves the fix (the relevant dbt test or
source freshness check).

## Detail (blockers and should_fix)

### 1. <title>

- Failure: <what goes wrong.>
- Evidence, re-validated: <file:line, quoted.>
- Resolution: <the concrete fix, carried forward to the implementing agent role on an after_fixes verdict.>
- Reproduce: `<execution command>`; verify with `<verification command>`.

## Findings dropped

<Findings from the panel that did not reproduce against the code, each with one line on why it was dropped. "None" when none.>

## Disagreements resolved

<Where reviewers conflicted, what the evidence showed, and the call made. "None" when none.>

## Escalations

<Decisions with material impact that the consolidator did not make, above all where the spec and the PRD disagree. "None" when none.>

## Coverage

<The combined coverage across the panel, and anything left unopened.>
