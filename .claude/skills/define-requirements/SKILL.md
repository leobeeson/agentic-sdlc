---
name: define-requirements
description: Phase 1 of the agentic SDLC, requirements definition. Use after the charter exists, to turn a vision into a product requirements document with stable requirement identifiers, MoSCoW priority, and Given/When/Then acceptance criteria. Converses with the developer through a full requirements interview (personas, journeys, functional and non-functional requirements, data rules, interfaces, constraints, assumptions, edge cases), and may spawn requirements-analyst subagents to fan out persona drafting, functional-requirement extraction, and edge-case enumeration in parallel. Run this once the charter is settled and you are ready to specify what the product must do.
---

# Define Requirements

Phase 1 of the pipeline. The charter from phase 0 says what the product is and why it is built. This phase says what it must do, precisely enough that phase 2 can design an architecture against it and phase 3 can plan tasks against it. The output is a product requirements document where every requirement carries a stable identifier, a MoSCoW priority, and acceptance criteria in a Given/When/Then grammar, so later phases can reference a requirement by id.

This is an interactive skill. It interviews the developer through a structured requirements checklist, and may spawn `requirements-analyst` subagents to fan out the heavier drafting (personas, functional requirements, edge cases) in parallel, then merges what they return into one document.

## What this skill reads from the profile

Everything project-specific is read at runtime from `sdlc.config.yaml` at the repository root. Resolve these before doing anything else. The defaults apply only when a field is absent.

- `artifact_root` (default `ai_docs`). All artifacts live under this tree. Prose below uses `ai_docs/`, but the value is always the configured root.

If `sdlc.config.yaml` is absent, note it in your completion summary, fall back to the default, and proceed.

## Inputs and outputs

Reads:

- `<artifact_root>/charter.md`, the phase 0 output: vision, objectives, success metrics, constraints, stakeholders, and risks. The requirements must serve the charter's objectives, honour its constraints, and be measurable against its success metrics.

Produces:

- `<artifact_root>/prd.md`, the product requirements document, matching the prd template.

## Identifiers and grammar

These are the discipline this phase adds, and they are not optional. Later phases reference requirements by id, so the ids must be stable and the acceptance criteria must be machine-checkable.

- Functional requirements are numbered `REQ-001`, `REQ-002`, `REQ-003`, in a single sequence. Each id, once assigned, is stable: it is the handle phase 2 and phase 3 use to trace work back to a requirement.
- Non-functional requirements are numbered `NFR-001`, `NFR-002`, in their own sequence, each with a measure and a target.
- Each functional requirement carries a MoSCoW priority: `must`, `should`, `could`, or `will-not`.
- Each functional requirement carries acceptance criteria in Given/When/Then form: `Given <state>, when <action>, then <observable result>.` A requirement is not done until its acceptance criteria are written and each one is observable and testable.

## Process

### 1. Read the charter

Read `<artifact_root>/charter.md` in full. Take the objectives, success metrics, constraints, stakeholders, and risks. The requirements you elicit must serve those objectives and stay inside those constraints. Carry the charter's constraints forward into the requirements document rather than restating the vision; the charter remains the source for what and why, and this document is what the product must do.

### 2. Interview the developer

Converse with the developer to turn the vision into specific, measurable, testable requirements. This is the valuable core kept from the older requirements consultant: a strong interview checklist, worked through interactively, that drives vague ideas into concrete statements. Cover each topic below. Confirm your understanding back to the developer as you settle each one, and propose structure rather than demanding the developer supply it from a blank page.

- **Product overview.** What the product does, in product terms, and for whom. One paragraph that anyone can read.
- **User personas.** Each distinct kind of user: name, goals, context, and the scenarios where they meet the product.
- **User journeys.** The end-to-end paths a persona takes through the product to reach an outcome. Each journey grounds the functional requirements that serve it.
- **Functional requirements.** What the product must do, as discrete capabilities. Drive each towards a statement of the form: as a `<persona>`, I want `<capability>` so that `<outcome>`.
- **Non-functional requirements.** Qualities the product must have: performance, scalability, availability, security, accessibility, maintainability. Each must have a measure and a target, never a vague adjective.
- **Data requirements and business rules.** Key entities, their relationships, and the rules that constrain behaviour (validation, lifecycle, invariants, retention).
- **Interface requirements.** The surfaces the product exposes or consumes: user interfaces, APIs, integrations with other systems, file or message formats.
- **Constraints.** Limits the product must respect, including those inherited from the charter: technical, regulatory, budget, timeline, platform.
- **Assumptions.** What you are taking as given that is not yet confirmed. Record each so the architecture phase can test it.
- **Acceptance criteria.** For each functional requirement, the observable conditions that mean it is satisfied, in Given/When/Then form.
- **Prioritisation.** A MoSCoW priority for every functional requirement: `must`, `should`, `could`, `will-not`. Drive the developer to name the will-nots explicitly, because the scope boundary is as informative as the scope.
- **Edge cases and error scenarios.** For each capability, what happens at the boundaries and when things go wrong: empty inputs, limits, concurrency, failures, malformed data, unauthorised access.

Ask focused questions, and turn every vague answer into a specific, measurable, testable statement before moving on. Do not pad the interview; once a topic is settled, move to the next.

### 3. Fan out the drafting

Once the interview has settled enough material, spawn `requirements-analyst` subagents to draft the heavier sections in parallel, rather than drafting them all sequentially yourself. The natural split is three independent strands, so spawn them in a single batch:

- **Personas and journeys.** Draft the persona set and the user journeys from the interview notes.
- **Functional requirements.** Draft the functional requirements as `REQ-NNN` entries, each with its statement, a proposed MoSCoW priority, and Given/When/Then acceptance criteria.
- **Edge cases and error scenarios.** Enumerate the boundary and failure cases for each capability, and surface the additional requirements or acceptance criteria they imply.

Give each analyst the relevant slice of the interview notes and the charter, and the conventions it must follow (the id schemes, the MoSCoW set, the Given/When/Then grammar, British English). Each analyst returns its drafted section. The analysts propose; they do not own the final ids. Wait for every analyst to complete before merging.

Fanning out is the default for a substantial product. For a small product where the strands are thin, drafting in the main context is acceptable; do not spawn analysts for the sake of it.

### 4. Merge and assign identifiers

Merge the returned drafts into one coherent set, then assign identifiers.

- Reconcile overlaps and contradictions between the strands. The edge-case analyst will often have implied requirements the functional strand also covers; fold them together rather than duplicating.
- Assign `REQ-NNN` ids in a single global sequence across the whole functional set. The analysts worked in their own terms; the final ids are assigned here so the document is internally consistent. Order the sequence so related requirements sit together where it helps the reader.
- Assign `NFR-NNN` ids to the non-functional requirements in their own sequence.
- Confirm every functional requirement has a MoSCoW priority and at least one Given/When/Then acceptance criterion, and that every criterion is observable and testable. Resolve any requirement that fails this back with the developer before writing.
- Trace coverage: every charter objective should be served by at least one requirement, and every requirement should trace back to an objective or a stated assumption. Flag any gap to the developer.

### 5. Write the requirements document

Write `<artifact_root>/prd.md` from the merged set, matching the prd template. The sections are:

- **Overview.** What the product does, in product terms, for whom.
- **Personas.** Each persona with name, goals, context, and the scenarios where they meet the product.
- **Functional requirements.** Each as a `REQ-NNN` entry with its short name, MoSCoW priority, a statement in the as a / I want / so that form, and acceptance criteria in Given/When/Then form.
- **Non-functional requirements.** A table of `NFR-NNN`, the requirement, and its measure and target.
- **Data and business rules.** Key entities, relationships, and the rules that constrain behaviour.
- **Constraints and assumptions.** Constraints inherited from the charter, and the assumptions made here.
- **Prioritised requirement list.** The full requirement set, ordered, with priority, as the input to architecture and planning.

## The handoff into design-architecture

Once `prd.md` exists, this phase is done and phase 2 takes over. `design-architecture` reads `prd.md` and designs an architecture that satisfies the requirements, referencing them by their `REQ-NNN` and `NFR-NNN` ids. The stable identifiers and the Given/When/Then acceptance criteria are the contract across the seam: the architecture is accountable to specific requirements, and the planning phase later traces every task back to the requirements it serves. This is why the ids must be stable and the criteria must be testable.

## Guidelines

### Do

- Resolve the profile first and use the configured `artifact_root` everywhere.
- Read the charter in full and keep every requirement serving its objectives and inside its constraints.
- Cover every topic in the interview checklist before writing.
- Turn every vague idea into a specific, measurable, testable requirement.
- Give every functional requirement a stable `REQ-NNN` id, a MoSCoW priority, and Given/When/Then acceptance criteria.
- Give every non-functional requirement an `NFR-NNN` id with a measure and a target.
- Name the will-not requirements explicitly, so the scope boundary is recorded.
- Spawn the requirements-analyst subagents concurrently for a substantial product, and wait for all of them before merging.
- Assign the final ids yourself after merging, so the document is internally consistent.

### Do not

- Hardcode a project specific. All coupling is read from `sdlc.config.yaml`.
- Leave any requirement without a priority or without observable acceptance criteria.
- Write a non-functional requirement as a vague adjective with no measure and target.
- Renumber requirements gratuitously once ids are assigned; the ids are the handle later phases depend on.
- Reopen the charter's vision; this document is what the product must do, not what or why.
- Reference any external tracker, the gh CLI, or a CI gate. The artifact tree is the system of record.

## Completion

Return a 3 line summary: the counts of functional requirements by MoSCoW priority and the count of non-functional requirements; the personas and the key scope boundary (the notable will-nots); and a pointer to `<artifact_root>/prd.md` as the handoff into `design-architecture`.
