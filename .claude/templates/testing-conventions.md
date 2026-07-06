<!-- TEMPLATE: the testing conventions of the project. Owner: the
     context-agent, the single writer of ai_docs/reference/. Path:
     ai_docs/reference/testing-conventions.md (the project spine). Every agent
     that reasons about tests reads this file: the task-preparer grounds the
     test plan in it, the generation roles follow it, and the test-adequacy
     reviewer judges against it. Setup seeds it from the detected or declared
     stack. Keep this file under 200 lines. -->

<!-- PROVENANCE (append-only; only created is fixed) -->
created:        <ISO-8601 timestamp>
modified:       [<ISO-8601 timestamp>]
commits:        [<short-sha>]
agents:         [context-agent]
run-ids:        [<run-id>]
back-refs:      [sdlc.config.yaml (validation.commands)]
forward-refs:   [task-briefs/, the generated tests]
<!-- END PROVENANCE -->

# Testing conventions

## Test commands

<The exact commands that run the suite. The authoritative copy is validation.commands in sdlc.config.yaml; this section explains when each applies.>

## Test naming

<The naming convention for tests (for example test_<behaviour>): the name describes what the system does, not how.>

## Cadence

<The development cadence (for example red, green, refactor in vertical slices: one behaviour at a time, never all tests first).>

## Mocking policy

<Where mocking is allowed (for example only at system boundaries: model calls, database, external HTTP, time and randomness), and the real defaults used in place of mocks.>

## Levels

<What unit, integration, and end-to-end mean in this project, and when each applies. For a data-engineering project: what dbt tests cover, what the framework's own validation covers, and what needs a bespoke check.>
