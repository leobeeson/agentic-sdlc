# Phase 1: Define Requirements

## Purpose

Phase 1 turns the vision into a precise statement of what the product must do. It produces the product requirements document, where every functional requirement carries a stable identifier, a MoSCoW priority, and acceptance criteria in a Given/When/Then grammar, and every non-functional requirement carries a measure and a target. The charter said what the product is and why; this phase says what it must do, precisely enough that phase 2 can design an architecture against it and phase 3 can plan tasks against it.

This is an interactive phase. It interviews the developer through a requirements checklist and may fan out the heavier drafting to subagents, then merges what they return into one document and owns the final identifiers.

## Inputs

- `sdlc.config.yaml`, resolved first, for `artifact_root` (default `ai_docs`).
- `<artifact_root>/charter.md`, the phase 0 output, read in full: the vision, objectives, success metrics, constraints, stakeholders, and risks. The requirements must serve those objectives and stay inside those constraints.

If `sdlc.config.yaml` is absent, the skill notes it, falls back to the default, and proceeds.

## What it produces

A single artifact, under the configured `artifact_root` (default `ai_docs`):

- `<artifact_root>/prd.md`, the product requirements document, matching `.claude/templates/prd.md`.

The document holds an overview, the personas, the functional requirements, the non-functional requirements, the data and business rules, the constraints and assumptions, and a prioritised requirement list. The disciplines this phase adds are not optional:

- Functional requirements are numbered `REQ-001`, `REQ-002`, in a single global sequence. Each id, once assigned, is stable: it is the handle phase 2 and phase 3 use to trace work back to a requirement.
- Non-functional requirements are numbered `NFR-001`, `NFR-002`, in their own sequence, each with a measure and a target.
- Each functional requirement carries a MoSCoW priority: `must`, `should`, `could`, or `will-not`.
- Each functional requirement carries acceptance criteria in Given/When/Then form, each criterion observable and testable.

## How to run

- Command: `/define-requirements`.
- Skill: `define-requirements`.
- Agents spawned: `requirements-analyst` subagents, to fan out the heavier drafting in parallel.

The skill reads the charter, then interviews the developer across the checklist: product overview, user personas, user journeys, functional requirements, non-functional requirements, data requirements and business rules, interface requirements, constraints, assumptions, acceptance criteria, prioritisation, and edge cases and error scenarios. Once enough material is settled, it spawns `requirements-analyst` subagents in a single batch over three independent strands: personas and journeys, functional requirements, and edge cases and error scenarios. Each analyst is read-only, drafts its slice in the requirement grammar, and returns the draft; it never owns the final ids. The skill then merges the drafts, reconciles overlaps, assigns the global `REQ-NNN` and `NFR-NNN` ids itself, confirms every requirement has a priority and observable acceptance criteria, traces coverage against the charter objectives, and writes `prd.md`.

For a small product where the strands are thin, drafting in the main context is acceptable; the analysts are not spawned for their own sake.

## What good output looks like

- Every functional requirement has a stable `REQ-NNN` id, a MoSCoW priority, a statement in the as a / I want / so that form, and at least one Given/When/Then acceptance criterion that a tester can check.
- Every non-functional requirement has an `NFR-NNN` id with a real measure and target, never a vague adjective.
- The will-not requirements are named explicitly, so the scope boundary is recorded as clearly as the scope.
- Every charter objective is served by at least one requirement, and every requirement traces back to an objective or a stated assumption. Gaps are flagged, not hidden.
- Vague ideas have been driven into specific, measurable, testable statements. Edge cases and failure modes are enumerated, not left at the happy path.
- The ids are assigned once and not renumbered gratuitously, because later phases depend on them as stable handles.

## Hand-off

Phase 2, `design-architecture`, consumes the requirements. It reads `<artifact_root>/prd.md` and designs an architecture that satisfies them, referencing each requirement by its `REQ-NNN` or `NFR-NNN` id. The stable identifiers and the Given/When/Then acceptance criteria are the contract across the seam: the architecture is accountable to specific requirements, and phase 3 later traces every task back to the requirements it serves.
