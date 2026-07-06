<!-- TEMPLATE: the implementation plan for one initiative. Owner: the
     implementation-planner skill (a gated consultation the main agent
     performs). Path: ai_docs/initiatives/<initiative-id>/implementation-plan.md
     (the initiative workspace). Reads architecture.md, the ADRs, and prd.md.
     This plan, together with the per-task specs under specs/ and the task
     registry specs/index.md, is the bridge into the generation stage. Replace
     every placeholder. -->

<!-- PROVENANCE (append-only; only created is fixed) -->
created:        <ISO-8601 timestamp>
modified:       [<ISO-8601 timestamp>]
commits:        [<short-sha>]
agents:         [implementation-planner]
run-ids:        [<run-id>]
back-refs:      [prd.md, architecture.md, reference/adrs/]
forward-refs:   [specs/index.md, specs/<spec-file>.md]
<!-- END PROVENANCE -->

# Implementation Plan: <initiative-id> <initiative title>

## Approach

<The build strategy in a few sentences, including what the first deliverable is.>

## Work breakdown

The areas of concern, each becoming a spec document `specs/NN-<area>.md`, and the tasks within each.

| Area | Spec document | Tasks |
| --- | --- | --- |
| <area> | specs/NN-<area>.md | TASK-NNN, TASK-NNN |

## Sequencing and dependencies

<The order tasks must be built in, and the dependencies between them.>

## First deliverable

<The smallest coherent set of tasks that produces something working end to end.>

## Testing strategy

<How tasks will be verified: the levels of testing, the validation commands drawn from sdlc.config.yaml, and the conventions captured in reference/testing-conventions.md.>

## Risks

| Risk | Affected tasks | Mitigation |
| --- | --- | --- |
| <risk> | <tasks> | <mitigation> |
