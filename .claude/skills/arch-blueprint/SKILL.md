---
name: arch-blueprint
description: |
  Produces the architecture document and its ADRs. Load after the PRD, when an intent changes
  the architectural design (a new component, a changed data flow, a new integration), or
  standalone from a direct brief. A gated consultation: explore, confirm, generate, refine.
  Spawns feature-explorer subagents, one per architectural question, to investigate
  trade-offs without flooding the conversation.
allowed-tools: Read, Grep, Glob, Bash, Write
model: opus
inputs:
  - name: prd
    required: false
    signal: the requirements, personas, and acceptance criteria the architecture must satisfy
    source: ai_docs/prd.md, written by the requirements-navigator agent
  - name: brief
    required: true if no prd
    signal: the developer's statement of what must be built; required directly when no PRD is present, so the agent can run standalone
    source: supplied inline by the developer, or a path the orchestrator binds
outputs:
  - type: architecture document
    location: ai_docs/architecture.md (the project spine)
  - type: architecture decision records
    location: ai_docs/reference/adrs/ (one ADR per significant decision)
preconditions: either a PRD or a direct brief must be present
intents:
  - ad-hoc code development (default new capability and above; at new feature when the intent changes the architectural design)
  - ADP Foundry YAML generation (default new capability and above; at new feature when the intent changes the architectural design)
  - dbt-model generation (default new capability and above; at new feature when the intent changes the architectural design)
scope: core
model_floor: strong
cost_tier: heavy
standalone: yes
idempotency: reuse an existing valid architecture.md and its ADRs rather than regenerating them; accept an externally produced architecture that carries the schema and a provenance header marked external
primitive: skill
phase: phase-1
---

# Arch Blueprint

The architecture consultation. It settles the architectural design and records the reasoning behind every significant decision as an ADR, so later agent roles and reviewers read the reasoning, not only the result. A wrong engineering specification is among the most expensive errors the pipeline can make, which is why this agent role runs on the strong tier.

This is a gated consultation performed by the main agent in the conversation: explore, confirm, generate, refine.

## Idempotency, checked first

Check `ai_docs/architecture.md` before anything else.

- The document exists and validates against `.claude/templates/architecture.md`: reuse it and move to refinement mode. When the classified intent changes the architectural design, refinement means designing the delta: the new component, the changed data flow, the new integration, recorded in the affected sections and in new ADRs, with the rest untouched.
- The document carries a provenance header marked external: accept it; propose edits rather than rewriting uninvited.
- The document is absent: run the consultation.

## Resolve the inputs

- Read `ai_docs/prd.md` when present: the REQ and NFR identifiers are what the architecture is accountable to. Every component must trace to the requirements it serves, and every must-have requirement must be served by a component.
- When no PRD exists, the brief binds directly (the standalone binding); record that in the provenance back-references.
- On an existing codebase, survey what is already there with Read, Grep, and Glob before designing: the current components and boundaries, the stores, the pipelines, the integration points, and the conventions in force. The architecture must fit what exists; the code is the source of truth for the current state.
- Read `ai_docs/reference/CONTEXT.md` and existing ADRs under `ai_docs/reference/adrs/` when present; do not resettle a decision an ADR already records without saying so.

## The consultation

Explore the topics below with the developer. Hold the mental graph: drill into a topic, then advance or backtrack as answers reopen earlier concerns. For each significant choice, present the realistic options with their trade-offs and a recommendation; never assert a single design where a genuine trade-off exists.

- **Vision and workloads.** What the system is for, the primary use cases and workloads, and the requirement identifiers each must satisfy.
- **Sources and ingestion.** Each source system, its delivery mechanism (file drop, API, replication, stream), cadence, and contract; the ingestion pattern per source and how late, duplicate, and malformed arrivals are handled.
- **Warehouse layering and modelling.** The layers (raw, staging, refined, marts, or the project's equivalents), the modelling approach per layer, naming conventions, and where each consumer reads.
- **Transformation and orchestration.** What transforms the data (dbt models, framework operators), what schedules and sequences the transformations (the orchestration DAGs), and how pipeline dependencies are expressed.
- **Data contracts between stages.** The schema, freshness, and quality guarantees each stage offers the next, and where a contract is checked.
- **Components and integration.** Any services or tooling beside the pipelines: their responsibilities, their interfaces, and what crosses each boundary.
- **Storage and retention.** The stores, their high-level schemas, partitioning, archival, and retention against the compliance obligations the charter records.
- **Security and trust boundaries.** Where the boundaries fall, what authenticates and authorises across them, how secrets and credentials are handled, and how personal or regulated data is protected.
- **Performance and cost.** The volumes and latencies the design must sustain, where the design scales, and where the cost concentrates.
- **Observability and data quality monitoring.** What is logged and measured, where data quality is tested, and how a failure or a quality breach is detected and diagnosed.
- **Deployment topology.** Environments, promotion between them, and how the generated artefacts reach the platform that runs them.
- **Future expansion.** The directions the design keeps open, and the choices that would foreclose them.

Settle immaterial points by inference; ask when the open readings would produce materially different designs.

## Fan-out: feature-explorer only

For a hard trade-off or an unfamiliar surface, spawn feature-explorer subagents, one per architectural question, in a single message: how a candidate storage layout behaves at the stated volumes, how the existing codebase implements a comparable integration, what an external framework's documentation says about a constraint. Each explorer returns evidence; you weigh the trade-off and settle the choice with the developer. All investigation fan-out is the feature-explorer, so the catalogue stays closed and the conversation stays clean of raw research.

## The confirmation gate

Withhold the document until every applicable topic is explored and the developer explicitly confirms completeness. Before asking, state: the settled decisions and their trade-offs, the coverage of must-have requirements by components, the decisions that will earn ADRs, and any point settled by inference worth reopening.

## Generate the architecture and the ADRs

Write `ai_docs/architecture.md` matching `.claude/templates/architecture.md`: overview with the requirement identifiers satisfied, components with responsibilities and the requirements each serves, interaction and data flow (with Mermaid diagrams under `ai_docs/diagrams/`, referenced from the document), data and storage, cross-cutting concerns, and the trade-offs table linking each settled choice to its ADR.

Create one ADR under `ai_docs/reference/adrs/` for each decision that passes all three bars: hard to reverse, surprising without context, and the result of a real trade-off. Name each `<number>-<slug>.md`, keep each to a few sentences (context, decision, why), and link every ADR from the trade-offs table. A choice that is easily reversed, obvious, or had no real alternative earns no record.

Fill the provenance headers, with back-references to the PRD or the direct brief.

## Refinement mode

Subsequent turns adjust specific sections and add ADRs in place. Never regenerate the whole document unless explicitly instructed; never rewrite an existing ADR to change history, because an ADR records a decision as made; a reversal is a new ADR that supersedes the old one. Append to the provenance `modified` list on each change.

## Guidelines

### Do

- Check idempotency first; design the delta on an existing architecture rather than reopening the whole design.
- Survey the existing codebase before designing, and design to fit it.
- Present options with trade-offs and a recommendation for every significant choice.
- Trace every component to requirement identifiers, and verify every must-have is served.
- Reserve ADRs for decisions passing all three bars, and record a reversal as a superseding ADR.

### Do not

- Generate before the double gate passes.
- Assert one design where a genuine trade-off exists.
- Reopen the requirements; when a requirement looks wrong, raise it, do not rework it here.
- Descend to task-level detail; decomposition belongs to the implementation-planner.
- Regenerate the whole document during refinement.

## Handoff

The implementation-planner reads `ai_docs/architecture.md`, the ADRs, and `ai_docs/prd.md`, and decomposes the settled design into ordered, self-contained task specs. In a hand-driven session the developer invokes `/implementation-planner` next.
