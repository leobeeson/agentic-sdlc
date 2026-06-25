---
name: design-architecture
description: Phase 2 of the agentic SDLC. Use after the requirements exist, to turn them into a system architecture. Converses with the developer to work through a broad architecture checklist, proposes technical alternatives with their trade-offs, and may spawn architecture-advisor subagents to evaluate hard trade-offs in parallel. Produces the architecture document, Mermaid diagrams, a seeded domain glossary, and decision records for choices that are hard to reverse. Can also scan an existing codebase to ground the design in what is already there. Run this once the requirements are settled and before planning the implementation.
---

# Design Architecture

Phase 2 of the pipeline. It reads the requirements and produces the system architecture: the document that says what the components are, how they interact, where the data lives, where the trust boundaries fall, and which technical choices were made and why. The architecture is the input to phase 3 (`plan-implementation`), which turns it into an implementation plan, spec documents, and the task registry.

This is an interactive skill. It interviews the developer through a broad architecture checklist, proposes alternatives with their trade-offs rather than asserting a single design, and spawns `architecture-advisor` subagents to evaluate hard trade-offs in parallel. On a brownfield project it scans the existing codebase with Read, Grep, and Glob so the design is grounded in what is already there.

## What this skill reads from the profile

Everything project-specific is read at runtime from `sdlc.config.yaml` at the repository root. Resolve these before doing anything else. The defaults apply only when a field is absent.

- `artifact_root` (default `ai_docs`). All artifacts live under this tree. Prose below uses `ai_docs/`, but the value is always the configured root.
- `reference.context_doc` (default `reference/CONTEXT.md`, relative to the artifact root). The domain glossary this phase seeds.
- `reference.adr_dir` (default `reference/adr`, relative to the artifact root). Where decision records are written.
- `project.kind` (`greenfield` or `brownfield`). On `brownfield`, scan the existing codebase before designing.

If `sdlc.config.yaml` is absent, note it in your completion summary, fall back to the defaults, and proceed.

## Inputs and outputs

Reads:

- `<artifact_root>/prd.md`, the phase 1 output, for requirement identifiers (REQ-00X), priorities, personas, and acceptance criteria.
- On a brownfield project, the existing codebase, to ground the architecture in the current structure.

Produces:

- `<artifact_root>/architecture.md`, the architecture document, matching the architecture template.
- Diagrams under `<artifact_root>/diagrams/`, as Mermaid (`.mmd` or fenced Mermaid in `.md`), referenced from the architecture document.
- A seed of the configured context doc (`reference.context_doc`), the domain glossary, matching the CONTEXT template.
- Decision records under the configured `reference.adr_dir`, one per qualifying choice, matching the ADR template.
- Optionally, other domain reference docs under `reference/` when a concern is large enough to deserve its own document.

## Process

### 1. Read the requirements and resolve the profile

Read `<artifact_root>/prd.md` in full. Take the requirement identifiers, their MoSCoW priorities, the personas, and the acceptance criteria. The architecture exists to satisfy the requirements, so every component you propose must trace back to the requirements it serves, and every must-have requirement must be served by some component. Resolve the profile fields above so you know where to write every output.

### 2. Scan the existing codebase, if brownfield

If `project.kind` is `brownfield`, scan the existing codebase with Glob, Grep, and Read before designing. Establish the current components and their boundaries, the stores already in use, the integration points, the conventions in force, and the constraints the existing system imposes. The architecture must fit what is already there, not pretend the repository is empty. Treat the code as the source of truth for the current state.

### 3. Interview the developer through the architecture checklist

Converse with the developer to settle the architecture. This is the valuable core kept from the older architecture consultant: a broad topic checklist, worked through interactively, with alternatives and their trade-offs proposed rather than a single design asserted. Cover each topic that applies to the system, in roughly this order, confirming your understanding back to the developer as you settle each one.

- **Overall vision and use cases.** What the system is for and the primary use cases it must serve, drawn from the charter and the requirements.
- **Components or services and their responsibilities.** The components the system decomposes into, each with a single clear responsibility and the requirements it serves.
- **Interaction and integration.** How components interact: synchronous calls, queues, streams, events. Where the boundaries are and what crosses them.
- **Endpoints and data flow.** The interfaces each component exposes and how data flows through the system end to end.
- **Technical alternatives and trade-offs.** For each significant choice, the realistic options, their trade-offs, and the recommendation. Propose alternatives; do not assert one design as the only option.
- **Data management and storage.** The stores, their schemas at a high level, caching, and retention.
- **External integrations.** The third-party systems and services the design depends on, and what each is relied on for.
- **Security and trust boundaries.** Where the trust boundaries fall, what authenticates and authorises across them, and how secrets are handled.
- **Performance and scalability.** The load the system must handle, where it scales, and the bottlenecks to design around.
- **Testing and quality strategy.** How the architecture supports testing, and the quality attributes it must hold to.
- **Deployment and infrastructure.** Where and how the system runs, and the infrastructure it needs.
- **Monitoring and observability.** What is logged, measured, and traced, and how a failure is detected and diagnosed.
- **Maintenance.** How the system is kept healthy over time, and what makes it easy or hard to change.
- **Future-proofing.** The directions the system is likely to grow, and the choices that keep those directions open.

Ask focused questions. Propose a structure rather than demanding the developer supply one from a blank page. Record decisions as you settle them. Do not pad the interview; once a topic is settled, move on. Skip a topic only when it genuinely does not apply to this system, and say so.

### 4. Evaluate hard trade-offs with architecture-advisor subagents

When a choice is a real trade-off with no obvious answer (synchronous versus asynchronous integration, one storage technology versus another, an integration or messaging pattern, a build versus buy decision), spawn `architecture-advisor` subagents to evaluate the options in parallel rather than reasoning through them serially in the main thread. These trade-offs are independent of one another, so spawn the advisors in a single batch and let them run concurrently.

Give each advisor the specific decision point, the realistic options, the relevant slice of the requirements and any constraints (load, latency, team familiarity, the existing stack on brownfield), and ask for the options with their trade-offs and a recommendation. Bring each advisor's analysis back into the interview, settle the choice with the developer, and feed the settled choices into the trade-offs table and, where the choice qualifies, into a decision record.

### 5. Draw the diagrams

Write the diagrams under `<artifact_root>/diagrams/` as Mermaid, so they render in any markdown viewer and stay in version control as text. Draw the diagrams the architecture actually needs, typically:

- A component or container diagram showing the components and the connections between them.
- One or more data-flow or sequence diagrams for the primary use cases, showing how a request moves through the system.

Name each diagram for what it shows. Reference every diagram from the architecture document so the prose and the diagrams stay together.

### 6. Write the architecture document

Write `<artifact_root>/architecture.md` from the settled interview, matching the architecture template. The sections are:

- **Overview.** The system in one paragraph, and the requirement identifiers it must satisfy.
- **Components.** For each component, its responsibility, the requirements it serves (REQ-00X), and the interfaces and endpoints it exposes.
- **Interaction and data flow.** How components interact (synchronous calls, queues, streams) and how data flows between them, referencing the diagrams under `diagrams/`.
- **Data and storage.** The stores, their schemas at a high level, caching, and retention.
- **Cross-cutting concerns.** Security and trust boundaries, scalability, observability, failure and recovery.
- **Trade-offs considered.** The table of decision point, options, choice, why, and a link to the decision record where one was created.
- **Decision records.** Links to the records under the configured `reference.adr_dir`.

Trace every component to the requirements it serves, and confirm every must-have requirement is served by a component.

### 7. Seed the domain glossary

Seed the configured context doc (`reference.context_doc`), matching the CONTEXT template. Add one entry per domain term that the architecture introduces or relies on: the components, the core domain concepts, and any term whose meaning is specific to this project. Each entry is the precise meaning of the term in this project, in one short paragraph. This is the ubiquitous language every later agent reads and uses exactly, so name things once and name them well. Keep the file under 200 lines. The `spec-reconciler` keeps it current as terms evolve; this phase establishes it.

Where a single concern is large enough to deserve its own reference document (a complex external integration, a non-trivial data model), seed it under `reference/<domain>.md` as well, and add its key terms to the glossary.

### 8. Record the hard-to-reverse decisions

Create a decision record under the configured `reference.adr_dir` for each decision that is all three of:

- **Hard to reverse.** Undoing it later would be costly, for example a primary datastore, a public interface contract, or a synchronous versus asynchronous integration spine.
- **Surprising without context.** A reader coming to the code later would not understand why it was done this way without the reasoning.
- **A real trade-off.** There was a genuine choice with costs on each side, not a default with no alternative.

A choice must be all three to earn a record. A choice that is easily reversed, or obvious, or had no real alternative, does not get one. Name each record `<number>-<slug>.md` (for example `001-event-bus-choice.md`), number them in a single sequence, and match the ADR template:

```
# <number>: <short title>

Context: the situation and the forces at play, in one or two sentences.
Decision: what was chosen.
Why: the trade-off that made this the choice, in one or two sentences.
```

Keep each record to a few sentences. Link every record from the trade-offs table and the decision records section of the architecture document.

## The handoff into plan-implementation

Once the architecture document, the diagrams, the seeded glossary, and the decision records exist, this phase is done and phase 3 takes over. `plan-implementation` reads `architecture.md` together with `prd.md`, takes the components, boundaries, integration points, and settled technical decisions as given, and turns them into the implementation plan, the spec documents, and the task registry. Settle the architecture here so that phase does not have to reopen it.

## Guidelines

### Do

- Resolve the profile first and use the configured `artifact_root`, `reference.context_doc`, and `reference.adr_dir` everywhere.
- Trace every component back to the requirements it serves, and check every must-have requirement is served.
- Propose alternatives with their trade-offs rather than asserting a single design.
- Spawn architecture-advisor subagents concurrently for the hard, independent trade-offs.
- On a brownfield project, scan the existing codebase and design to fit it.
- Write diagrams as Mermaid under `diagrams/` and reference them from the document.
- Seed the glossary with the ubiquitous language so later agents use the terms exactly.
- Reserve decision records for choices that are hard to reverse, surprising without context, and a real trade-off, all three.

### Do not

- Hardcode a project specific. All coupling is read from `sdlc.config.yaml`.
- Reference any external tracker, the gh CLI, or a CI gate.
- Write a decision record for a choice that is easily reversed, obvious, or had no real alternative.
- Reopen the requirements; if the requirements are wrong, raise it, do not silently rework them here.
- Assert one design when there is a genuine trade-off; surface the options and settle them with the developer.
- Let the glossary drift past 200 lines or carry one entry per trivial term.

## Completion

Return a 3 line summary: the components in the architecture and the requirement identifiers they cover; the diagrams written and the number of decision records created; and a pointer to `architecture.md` as the handoff into `plan-implementation`.
