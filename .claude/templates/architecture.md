<!-- TEMPLATE: the architecture document. Owner: the arch-blueprint skill (a
     gated consultation the main agent performs). Path: ai_docs/architecture.md
     (the project spine, singular, updated in place). Reads prd.md, or the
     developer's brief when no PRD exists. Decisions that are hard to reverse
     are recorded as architecture decision records under
     ai_docs/reference/adrs/. Replace every placeholder. -->

<!-- PROVENANCE (append-only; only created is fixed) -->
created:        <ISO-8601 timestamp>
modified:       [<ISO-8601 timestamp>]
commits:        [<short-sha>]
agents:         [arch-blueprint]
run-ids:        [<run-id>]
back-refs:      [prd.md]
forward-refs:   [reference/adrs/, initiatives/<initiative-id>/implementation-plan.md]
<!-- END PROVENANCE -->

# System Architecture: <project name>

## Overview

<The system in one paragraph, and the requirement identifiers it must satisfy.>

## Components

For each component or service: responsibility, the requirements it serves, and the interfaces it exposes.

### <component name>

- Responsibility: <what this component owns>
- Serves: REQ-00X, REQ-00Y
- Interfaces and endpoints: <what it exposes>

## Interaction and data flow

<How components interact (synchronous calls, queues, streams), and how data flows between them. Reference diagrams under ai_docs/diagrams/.>

## Data and storage

<Stores, schemas, caching, and retention.>

## Cross-cutting concerns

<Security and trust boundaries, scalability, observability, failure and recovery.>

## Trade-offs considered

| Decision point | Options | Choice | Why | Decision record |
| --- | --- | --- | --- | --- |
| <point> | <options weighed> | <choice> | <the trade-off> | reference/adrs/<number>-<slug>.md |

## Decision records

<Links to the records under ai_docs/reference/adrs/ created for hard-to-reverse choices.>
