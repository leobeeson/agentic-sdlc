<!-- TEMPLATE: the product requirements document. Owner: the
     requirements-navigator skill (a gated consultation the main agent
     performs). Path: ai_docs/prd.md (the project spine, singular, updated in
     place). Reads charter.md, or the developer's brief when no charter exists.
     Every requirement carries a stable identifier so later stages can reference
     it. Replace every placeholder. -->

<!-- PROVENANCE (append-only; only created is fixed) -->
created:        <ISO-8601 timestamp>
modified:       [<ISO-8601 timestamp>]
commits:        [<short-sha>]
agents:         [requirements-navigator]
run-ids:        [<run-id>]
back-refs:      [charter.md]
forward-refs:   [architecture.md, initiatives/<initiative-id>/implementation-plan.md]
<!-- END PROVENANCE -->

# Product Requirements: <project name>

## Overview

<What the product does, in product terms, for whom.>

## Personas

<For each persona: name, goals, context, and the scenarios where they meet the product.>

## Functional requirements

Each requirement has an identifier, a statement, a MoSCoW priority, and acceptance criteria.

### REQ-001: <short name>

- Priority: must | should | could | will-not
- Statement: as a <persona>, I want <capability> so that <outcome>.
- Acceptance criteria (Given/When/Then):
  - Given <state>, when <action>, then <observable result>.

## Non-functional requirements

| Identifier | Requirement | Measure and target |
| --- | --- | --- |
| NFR-001 | <requirement> | <measure and target> |

## Data and business rules

<Key entities, relationships, and rules that constrain behaviour.>

## Constraints and assumptions

- <Constraints inherited from the charter, and assumptions made here.>

## Prioritised requirement list

<The full requirement set, ordered, with priority, as the input to architecture and planning.>
