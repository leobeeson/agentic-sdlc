<!-- TEMPLATE: the run record, one file per run at
     ai_docs/initiatives/<initiative-id>/run-record/<run-id>.md.
     Single writer: the orchestrator, which writes it throughout the run and
     closes it at the end. The run record exists because the orchestrator
     composes the plan dynamically: a developer who expected ten agent roles to
     run can read that six ran, which four did not, and why. It is the audit
     trail of the run and the state a fresh session rebuilds from.
     Phase 1 carries the fields below; the isolation, compute, and telemetry
     fields are deferred to Phase 2. -->

# Run record: <run-id>

- **Initiative:** <initiative-id>
- **Detected intent:** target <target>; magnitude <magnitude, or "not applicable">
- **Model dial:** <base | full> (set once at classification, from the magnitude)
- **Recipe selected:** <recipe family and magnitude key, or "dynamic decomposition: no recipe fit">
- **Status:** <open | complete | halted at <stage>>

## The composed execution plan

The ordered stages this run keeps, with one line of rationale per inclusion and
exclusion, written before anything executes.

| # | Stage | Agent role | Decision | Rationale |
| --- | --- | --- | --- | --- |
| 1 | <stage> | <agent role> | included | <e.g. "the intent changes what the product must do"> |
| — | <stage> | <agent role> | excluded | <pruned by magnitude \| skipped by idempotency \| disabled by configuration \| selected out by risk> |

## Degradation statements

<When composition pruned a stage whose output a later stage would read: what
will be degraded, and what would avoid the degradation. "None" when none.>

## Stage outcomes

Appended as the run proceeds, one row per stage that ran.

| Stage | Agent role | Outcome | Note |
| --- | --- | --- | --- |
| <stage> | <agent role> | <ran \| reused \| failed> | <artefact path; escalations triaged; gate outcomes> |

## Escalations and gate decisions

<Every escalation triaged during the run: the question, who resolved it (the
orchestrator from the run's own context, or the developer at a pause), and the
resolution. Every human gate: where the run paused and what the developer
decided. "None" when none.>
