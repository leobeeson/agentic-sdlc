# System Architecture: <project name>

Produced in phase 2 by the `design-architecture` skill. Reads the requirements document. Decisions that are hard to reverse are recorded as decision records under the configured `reference.adr_dir`.

## Overview

The system in one paragraph, and the requirement identifiers it must satisfy.

## Components

For each component or service: responsibility, the requirements it serves, and the interfaces it exposes.

### <component name>

- Responsibility:
- Serves: REQ-00X, REQ-00Y
- Interfaces and endpoints:

## Interaction and data flow

How components interact (synchronous calls, queues, streams), and how data flows between them. Reference diagrams under `diagrams/`.

## Data and storage

Stores, schemas, caching, and retention.

## Cross-cutting concerns

Security and trust boundaries, scalability, observability, failure and recovery.

## Trade-offs considered

| Decision point | Options | Choice | Why | Decision record |
|----------------|---------|--------|-----|-----------------|

## Decision records

Links to the records under the configured `reference.adr_dir` created for hard-to-reverse choices.
