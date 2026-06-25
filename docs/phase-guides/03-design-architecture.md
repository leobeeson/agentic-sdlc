# Phase 2: Design Architecture

## Purpose

Phase 2 turns the requirements into a system architecture. It produces the architecture document, which says what the components are, how they interact, where the data lives, where the trust boundaries fall, and which technical choices were made and why. It also seeds the domain glossary, draws the diagrams, and records the decisions that are hard to reverse. The architecture is the design phase 3 plans tasks against.

This is an interactive phase. It interviews the developer through a broad architecture checklist, proposes alternatives with their trade-offs rather than asserting a single design, and spawns subagents to evaluate the hard trade-offs in parallel. On a brownfield project it scans the existing codebase so the design fits what is already there.

## Inputs

- `sdlc.config.yaml`, resolved first, for `artifact_root` (default `ai_docs`), `reference.context_doc` (default `reference/CONTEXT.md`, the glossary this phase seeds), `reference.adr_dir` (default `reference/adr`, where decision records are written), and `project.kind` (scan the existing codebase when brownfield).
- `<artifact_root>/prd.md`, the phase 1 output, read in full: the requirement identifiers, their MoSCoW priorities, the personas, and the acceptance criteria.
- On a brownfield project, the existing codebase, to ground the architecture in the current structure, stores, integration points, and conventions.

If `sdlc.config.yaml` is absent, the skill notes it, falls back to the defaults, and proceeds.

## What it produces

Under the configured `artifact_root` (default `ai_docs`):

- `<artifact_root>/architecture.md`, the architecture document, matching `.claude/templates/architecture.md`. Its sections are an overview, the components, interaction and data flow, data and storage, cross-cutting concerns, a trade-offs table, and links to the decision records.
- Diagrams under `<artifact_root>/diagrams/`, written as Mermaid so they render in any markdown viewer and stay diffable in version control, referenced from the architecture document.
- A seed of the configured context doc (`reference.context_doc`), the domain glossary, matching `.claude/templates/CONTEXT.md`, with one entry per domain term the architecture introduces or relies on. Kept under 200 lines.
- Decision records under the configured `reference.adr_dir`, one per qualifying choice, named `<number>-<slug>.md` and matching `.claude/templates/adr.md`.
- Optionally, other domain reference docs under `reference/<domain>.md` when a single concern is large enough to deserve its own document.

## How to run

- Command: `/design-architecture`.
- Skill: `design-architecture`.
- Agents spawned: `architecture-advisor` subagents, to evaluate hard, independent trade-offs in parallel.

The skill reads the requirements and resolves the profile, scans the codebase if the project is brownfield, then interviews the developer across the checklist: overall vision and use cases, components and their responsibilities, interaction and integration, endpoints and data flow, technical alternatives and trade-offs, data management and storage, external integrations, security and trust boundaries, performance and scalability, testing and quality strategy, deployment and infrastructure, monitoring and observability, maintenance, and future-proofing. When a choice is a real trade-off with no obvious answer (synchronous versus asynchronous, one store versus another, build versus buy), it spawns `architecture-advisor` subagents in a single batch, one per decision point. Each advisor is read-only, draws its evaluation criteria from the requirements, cites a source for every external claim and a `file:line` for every claim about the existing system, recommends one option, and assesses reversibility. The skill weighs each recommendation, settles the choice with the developer, draws the diagrams, writes the architecture document, seeds the glossary, and records the qualifying decisions.

## What good output looks like

- Every component traces to the requirements it serves, and every must-have requirement is served by a component.
- Real alternatives were surfaced with their trade-offs and settled with the developer, not a single design asserted as the only option.
- The diagrams are Mermaid, named for what they show, and referenced from the prose so the document and the diagrams stay together.
- The glossary names the ubiquitous language once and names it well, so every later agent uses the terms exactly. It stays under 200 lines and carries no entry for a trivial term.
- A decision record exists for each choice that is all three of hard to reverse, surprising without context, and a real trade-off, and for no choice that is easily reversed, obvious, or had no alternative. Each record is a few sentences and is linked from the trade-offs table.
- The requirements are not reopened. If a requirement is wrong, it is raised, not silently reworked here.

## Hand-off

Phase 3, `plan-implementation`, consumes the architecture together with the requirements. It reads `architecture.md` and `prd.md`, takes the components, boundaries, integration points, and settled technical decisions as given, and turns them into the implementation plan, the spec documents, and the task registry. The glossary seeded here is read by every implementation-phase agent. The architecture is settled here so phase 3 does not have to reopen it.
