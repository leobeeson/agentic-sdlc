<!-- TEMPLATE: the per-task specification, the self-contained work order the
     generation stage executes. Owner: the implementation-planner skill (one
     spec per task, written at decomposition). Path:
     ai_docs/initiatives/<initiative-id>/specs/<spec-file>.md, indexed by the
     task registry specs/index.md. The spec is at once a durable artefact on the
     artefact bus and the prompt the implementation executes: the filled
     template is handed to the generating agent role as its work order. The
     placeholders carry the schema; the single instruction that turns this
     template into an artefact is: replace every placeholder. A template is
     guidance for quality and interoperability, not a hard gate: a missing or
     extra section is flagged rather than rejected. -->

<!-- PROVENANCE (append-only; only created is fixed) -->
created:        <ISO-8601 timestamp>
modified:       [<ISO-8601 timestamp>]
commits:        [<short-sha>]
agents:         [implementation-planner]
run-ids:        [<run-id>]
back-refs:      [implementation-plan.md, prd.md (REQ-00X), architecture.md]
forward-refs:   [explorations/<task-id>.md, task-briefs/<task-id>.md]
<!-- END PROVENANCE -->

# Task: <task name>

**Task identifier:** <task-id>
**Serves:** REQ-00X, REQ-00Y
**Dependencies:** <task-id, or none>
**Status:** planned | in-progress | implemented | reconciled

## Task Description

<Describe the task in detail: what must be built or changed, the behaviour it
must have, and how completion is judged. Carry the acceptance criteria forward
from the PRD in Given/When/Then form:>

- Given <state>, when <action>, then <observable result>.

## Relevant Files

<List the files relevant to the task, each with one line on why it matters.
List files to be created under an h3 'New Files' section.>

### New Files

- <path> : <what it will contain>

## Step by Step Tasks

IMPORTANT: Execute every step in order, top to bottom.

### 1. <step name>

- <the concrete actions of this step>

### 2. <step name>

- <the concrete actions of this step>

### N. Run the Validation Commands

- Run every command in the Validation Commands section and fix failures until every command passes.

## Validation Commands

<Commands that validate the task is complete with zero regressions; every
command must run without errors. Draw from the validation.commands slice of
sdlc.config.yaml and make each concrete for this task.>

- `dbt build --select <model>` - build and test the affected models
- `<further command>` - <what it proves>

## Notes

<Optional additional notes or context: constraints from ADRs, out-of-scope
statements naming the task that covers each deferred item, profile-specific
sections (an ADP Foundry YAML specification section, a dbt model specification
section) as the target requires.>
