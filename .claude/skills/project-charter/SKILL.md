---
name: project-charter
description: |
  Produces the project charter from a developer brief or a brownfield scan. Load at the start
  of a new project, when an intent extends the project's recorded purpose, scope, or
  constraints, or standalone, to fix what the project is for before any requirements or
  architecture work begins. A gated consultation: explore, confirm, generate, refine.
allowed-tools: Read, Grep, Glob, Bash, Write
inputs:
  - name: brief
    required: true
    signal: the developer's statement of what the project is for, its scope, and its constraints; may be a long document, a short note, or one typed paragraph
    source: supplied inline by the developer, or a path the orchestrator binds
  - name: brownfield_scan
    required: false
    signal: a survey of an existing codebase that substitutes for a brief when the project already exists
    source: the skill's own survey of the existing codebase, grounded by sdlc.config.yaml; no scan artefact is persisted in the tree
outputs:
  - type: project charter
    location: ai_docs/charter.md (the project spine)
preconditions: a brief or a brownfield scan must be present; nothing upstream is required
intents:
  - ad-hoc code development (new project and new capability magnitudes)
  - ADP Foundry YAML generation (new project and new capability magnitudes)
  - dbt-model generation (new project and new capability magnitudes)
scope: core
model_floor: mid
cost_tier: moderate
standalone: yes
idempotency: reuse an existing valid charter.md rather than regenerating it; accept an externally produced charter that carries the schema and a provenance header marked external
primitive: skill
phase: phase-1
---

# Project Charter

The highest-altitude consultation. The charter fixes what the project is for, its scope, and its constraints, before any requirements or architecture work begins. The charter is what and why the project is built; `sdlc.config.yaml` is how the project is built, and the profile already exists when this skill runs.

This is a gated consultation performed by the main agent in the conversation. The shape is fixed: explore the topics with the developer, confirm the exploration is complete, only then generate the document, and refine the document afterwards. The document is the residue of the conversation; no autonomous run could produce it without substituting derived assumptions for the developer's answers.

## Idempotency, checked first

Before anything else, check `ai_docs/charter.md`.

- The charter exists and validates against `.claude/templates/charter.md` (every required section present): reuse it. State its vision line to the developer and move straight to refinement mode. Regenerate only when the developer explicitly asks, and then overwrite in place while appending a new modified entry to the provenance header, so lineage survives the rebuild.
- The charter exists with a provenance header marked external: accept it as the charter. Do not rewrite an externally supplied charter uninvited.
- The charter is absent: run the consultation below.

## Resolve the inputs

- Read `sdlc.config.yaml` for `project.name`, `project.kind`, `project.stack`, and `artefact_tree.root`. Seed the consultation from these rather than asking the developer to repeat what the profile records.
- Resolve the brief as a semantic signal, not a format: the developer may supply a long document, a short note, a path, or one dictated paragraph. When no brief arrived and the repository holds an existing codebase, perform the brownfield scan: read the README, the top-level structure, the dependency and pipeline manifests, and any design notes, and treat what the code shows as the draft answers the developer corrects. The scan is your own work inside this stage; persist no scan artefact.
- When neither a brief nor an existing codebase is present, elicit the brief: ask what the project is for, in one or two sentences, and build from there. Never reject the run for a missing format.

## The consultation

Explore the topics below with the developer, question by question. Hold a mental graph of the topics: drill into one until it is settled, then advance to the next or backtrack to the parent concern the answer reopened. Offer candidate answers the developer can correct rather than demanding answers from a blank page, and confirm your understanding back as each topic settles.

- **Vision and purpose.** What the project is and the single statement of what success looks like. Drive towards one clear sentence.
- **Objectives and success metrics.** Each objective paired with a measurable metric and a target. An objective without a metric and a target is not yet settled.
- **Scope and explicit non-scope.** What the project delivers, and what the project deliberately does not deliver. The boundary is as informative as the content.
- **Stakeholders.** Who has an interest, their interest, and their influence: the sponsor, the users of the data products, the upstream source owners, the platform team, and anyone who can block or accelerate the work.
- **Constraints.** People, budget, deadlines, and the technical constraints of the platform: the approved stack, the warehouse, the orchestration framework, the environments.
- **Regulatory and compliance considerations.** The obligations the project must meet: data protection, sector regulation, retention rules, audit requirements. In a pharmaceutical data-engineering context this topic is rarely empty; omit it only when the developer confirms nothing applies.
- **Initial risks.** The few risks that genuinely matter, each with likelihood, impact, and mitigation, not an exhaustive list.
- **Timeline and milestones.** The dates that are fixed from outside, and the milestones the work answers to.
- **Future growth.** Where the project is expected to grow, so early decisions do not foreclose the growth.

Settle a point by inference when the point has no material impact; ask when the open readings would produce materially different charters, and ask again when the answer leaves the material point unresolved. A question with material impact is never settled by assumption. Do not pad the consultation: once a topic is settled, move on, and omit a topic that genuinely does not apply, saying so.

## The confirmation gate

Withhold the document until both halves of the gate pass: every applicable topic above has been explored, and the developer explicitly confirms the exploration is complete. Before asking for that confirmation, state the topics you consider settled, the topics you omitted and why, and any point you settled by inference that the developer may want to reopen. The confirmation is this stage's gate; no completion summary is returned, because the main agent performed the work itself.

## Generate the charter

Write `ai_docs/charter.md` from the settled topics, matching `.claude/templates/charter.md`: vision, objectives and success metrics, scope, stakeholders, constraints, and risks, with compliance obligations placed under constraints or risks by their nature and future growth under the vision or next steps. Fill the provenance header: `created` fixed once, `agents: [project-charter]`, the run identifier, and back-references to the brief or the surveyed codebase. Replace every placeholder; invent no section the template does not carry.

## Refinement mode

After the draft lands, subsequent turns discuss, adjust, and finalise specific sections. Edit the affected section in place; never regenerate the whole document unless the developer explicitly instructs it. Append to the provenance header's `modified` list on each change.

## Guidelines

### Do

- Check idempotency first and move straight to refinement mode on an existing valid charter.
- Ground a brownfield charter in the surveyed code, and treat the survey's findings as draft answers for the developer to correct.
- Insist on measurable success metrics, each with a target.
- Record the explicit non-scope; later stages depend on the boundary.
- Keep the charter at charter altitude: what and why, never component design or technology selection.

### Do not

- Generate the document before the confirmation gate passes.
- Regenerate the whole document during refinement; edit the affected sections in place.
- Settle a point with material impact by assumption.
- Persist any scan artefact; the charter is this stage's only output.
- Reference an external tracker or CI gate; the artefact tree is the system of record.

## Handoff

The charter is the first artefact of the project spine. The requirements-navigator reads `ai_docs/charter.md` as its framing input; when the orchestrator composed this stage, it continues the plan, and in a hand-driven session the developer invokes `/requirements-navigator` next.
