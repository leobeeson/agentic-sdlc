---
name: initialise-project
description: Phase 0 of the agentic SDLC, project initialisation. Use at the very start of a project, once the profile (sdlc.config.yaml) exists, to fix the vision and constraints before any technical work begins. Interviews the developer across vision, business objectives and measurable success metrics, stakeholders, market and competitive positioning, resource and timeline constraints, initial risks, regulatory and compliance considerations, ethical considerations, and future growth, then proposes the project charter. May spawn a research subagent for market or competitor scanning. Run this once before define-requirements.
---

# Initialise Project

Phase 0 of the pipeline, and the first phase a developer runs. It produces the project charter, the document that fixes vision and constraints before any technical work begins. The charter is what and why the project is built. The profile (`sdlc.config.yaml`) is how it is built, and it already exists at this point, produced earlier by the setup skill, because every agent including this one reads it.

This is an interactive skill. Its spine is a dialogue: it interviews the developer to sufficient confidence across a checklist of topics, then proposes a charter draft for the developer to refine. It may optionally spawn a research subagent for market or competitor scanning, but the conversation is the backbone and the research only feeds it.

## What this skill reads from the profile

Everything project-specific is read at runtime from `sdlc.config.yaml` at the repository root. Resolve these before doing anything else. The defaults apply only when a field is absent.

- `artifact_root` (default `ai_docs`). All artifacts live under this tree. Prose below uses `ai_docs/`, but the value is always the configured root.
- `project.name`, `project.description`, and `project.kind` (greenfield or brownfield). Seed the interview from these rather than asking the developer to repeat what the profile already states.

If `sdlc.config.yaml` is absent, note it in your completion summary, fall back to the defaults, and proceed.

## Output

A single artifact:

- `<artifact_root>/charter.md`, the project charter, matching the charter template under `.claude/templates/charter.md`.

This is the input to phase 1, `define-requirements`.

## Orient before the interview

Before asking anything, gather what is already known so the interview starts informed rather than from a blank page.

- Read the profile and take `project.name`, `project.description`, and `project.kind`.
- If a repository is already present (a brownfield project, or any existing code on disk), scan it with Read, Grep, and Glob to understand what exists: the README, top-level structure, the dependency manifests, and any existing product or design notes. This grounds the interview in the real starting point rather than a hypothetical one.
- Note whether the project looks like an internal tool or an externally facing product, because that decides which checklist topics apply.

## Interview the developer

Converse with the developer to reach sufficient confidence on the charter. This is the valuable core kept from the older initialisation consultant: a strong topic checklist, worked through interactively. Cover each topic below, adapted intelligently to the project, and omit any that genuinely do not apply to an internal tool (for an internal tool, market and competitive positioning usually does not apply, and regulatory considerations may not).

- **Vision and purpose.** What the project is and the single statement of what success looks like. Drive towards one clear sentence of vision.
- **Business objectives and success metrics.** The objectives the project serves, each paired with a measurable metric and a target. Push for measurability: an objective without a metric and a target is not yet settled.
- **Stakeholders.** Who has an interest in the project, their interest, and their influence. Cover sponsors, users, and anyone who can block or accelerate the work.
- **Market and competitive positioning.** How the project fits the landscape and what differentiates it. Omit for an internal tool.
- **Resource and timeline constraints.** The people, budget, deadlines, and technical constraints the project must work within.
- **Initial risk assessment.** What could go wrong, how likely it is, the impact, and the mitigation. Aim for the few risks that genuinely matter, not an exhaustive list.
- **Regulatory and compliance considerations.** Any laws, standards, or contractual obligations the project must meet (data protection, sector regulation, accessibility). Omit only when none apply.
- **Ethical considerations.** The ways the project could cause harm, and how that is guarded against (fairness, transparency, misuse, data handling).
- **Future growth and scalability.** Where the project is expected to grow, and the scalability the charter should anticipate so early decisions do not foreclose it.

Run the interview well:

- Ask focused questions and propose a structure rather than demanding the developer fill a blank page. Offer a candidate answer the developer can correct.
- Confirm your understanding back as you settle each topic, and record decisions as you go.
- Do not pad the interview. Once a topic is settled, move on. Stop interviewing when you have enough to draft a coherent charter, not when every conceivable question is exhausted.
- Do not withhold the draft until told to produce it. Interview to sufficient confidence, then propose the charter.

## Optional research subagent

When the project is externally facing and its market or competitive positioning is unclear, you may spawn a research subagent to scan the landscape, then fold its findings into the interview. Use WebSearch and WebFetch through the subagent to investigate competitors, comparable products, and market context. This is optional and supplementary: skip it for an internal tool, and never let it replace the dialogue. Bring the findings back to the developer for confirmation rather than treating them as settled fact, and proceed without it if research is inconclusive.

## Propose the charter

Once the interview has reached sufficient confidence, write `<artifact_root>/charter.md` from the settled topics, matching the charter template. The sections are:

- **Executive summary.** Two or three sentences: what the project is and why it exists.
- **Vision.** The single sentence statement of what success looks like.
- **Business objectives and success metrics.** Each objective paired with a measurable metric and a target.
- **Stakeholders.** A table of stakeholder, interest, and influence.
- **Market and positioning.** How the project fits the landscape and what differentiates it. Omit for an internal tool.
- **Constraints.** Resource, timeline, technical, regulatory, and compliance constraints.
- **Initial risks.** A table of risk, likelihood, impact, and mitigation.
- **Next steps.** The immediate actions that lead into the requirements phase.

Fold ethical considerations and future growth into the charter where they have weight: ethical considerations belong with constraints or risks depending on their nature, and future growth belongs in the vision or the next steps. Do not invent a section the template does not have; place the content where it fits.

Present the draft to the developer, take their corrections, and revise in place until they are satisfied. The charter is theirs, not a fixed output.

## The handoff into define-requirements

Once the charter exists and the developer is satisfied, this phase is done. The charter is the input to phase 1: `define-requirements` reads `<artifact_root>/charter.md` and elicits the requirements, personas, and acceptance criteria that realise the vision and objectives the charter fixes. The next steps section of the charter should point at that phase.

## Guidelines

### Do

- Resolve the profile first and use the configured `artifact_root` everywhere.
- Seed the interview from the profile and any existing repository, not a blank page.
- Cover every applicable checklist topic, adapted to the project, omitting only those that do not apply to an internal tool.
- Insist on measurable success metrics, each with a target.
- Interview to sufficient confidence, then propose the charter draft.
- Keep the charter consistent with the template, and place ethical and growth content where it fits.
- Treat any research findings as input for the developer to confirm, not settled fact.

### Do not

- Hardcode a project specific. All coupling is read from `sdlc.config.yaml`.
- Reference any external tracker, the gh CLI, or a CI gate. The artifact tree is the system of record.
- Withhold the charter draft until explicitly instructed; interview to confidence, then propose it.
- Pad the interview with questions that do not change the charter, or force market and regulatory topics onto an internal tool where they do not apply.
- Begin technical design here. The charter fixes what and why; the how starts in later phases.

## Completion

Return a 3 line summary: the vision in one line; the count of business objectives with metrics, stakeholders, and initial risks captured; and a pointer to `<artifact_root>/charter.md` as the handoff into `define-requirements`.
