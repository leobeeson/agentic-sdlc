# Phase 0: Initialise Project

## Purpose

Phase 0 fixes the project's vision and constraints before any technical work begins. It produces the charter, the document that states what the project is and why it exists: the vision, the business objectives with measurable success metrics, the stakeholders, the constraints, and the initial risks. The charter is the anchor every later phase traces back to. The profile fixed how the project is built; the charter fixes what and why.

This is an interactive phase. Its backbone is a dialogue: the skill interviews the developer to sufficient confidence across a topic checklist, then proposes a charter draft for the developer to refine.

## Inputs

- `sdlc.config.yaml` at the repository root, resolved first. It reads `artifact_root` (default `ai_docs`) to know where to write, and `project.name`, `project.description`, and `project.kind` to seed the interview rather than asking the developer to repeat what the profile already states.
- The existing repository, if one is present. On a brownfield project, or wherever code is already on disk, the skill scans the README, the top-level structure, the dependency manifests, and any existing product or design notes, so the interview starts from the real starting point rather than a blank page.

This is the first content phase, so it reads no prior pipeline artifact beyond the profile. If `sdlc.config.yaml` is absent, the skill notes it, falls back to the defaults, and proceeds.

## What it produces

A single artifact, under the configured `artifact_root` (default `ai_docs`):

- `<artifact_root>/charter.md`, the project charter, matching `.claude/templates/charter.md`.

The charter sections are an executive summary, the vision as a single sentence, the business objectives each paired with a measurable metric and a target, a stakeholders table, market and positioning (omitted for an internal tool), constraints, an initial risks table, and next steps. Ethical considerations and future growth are folded in where they have weight rather than given invented sections.

## How to run

- Command: `/initialise-project`.
- Skill: `initialise-project`.
- Agents spawned: optionally a research subagent for market or competitor scanning, when the project is externally facing and its positioning is unclear. This is supplementary and never replaces the dialogue.

The skill orients itself from the profile and any existing repository, then interviews the developer across the checklist: vision and purpose, business objectives and success metrics, stakeholders, market and competitive positioning, resource and timeline constraints, the initial risk assessment, regulatory and compliance considerations, ethical considerations, and future growth. It adapts the checklist to the project, omitting topics that genuinely do not apply to an internal tool. Once the interview reaches sufficient confidence, it proposes the charter draft and revises it in place with the developer until they are satisfied.

## What good output looks like

- The vision is a single clear sentence of what success looks like, not a paragraph of ambition.
- Every business objective is paired with a measurable metric and a target. An objective with no metric is not yet settled.
- The stakeholders cover sponsors, users, and anyone who can block or accelerate the work, each with their interest and influence.
- The initial risks are the few that genuinely matter, each with a likelihood, an impact, and a mitigation, not an exhaustive list.
- The constraints are real: resource, timeline, technical, and, where they apply, regulatory and compliance limits the project must work within.
- The interview is not padded. Settled topics move on, and topics that do not apply to an internal tool are omitted rather than forced.
- The charter is the developer's, refined with them, not a fixed output asserted at them.

## Hand-off

Phase 1, `define-requirements`, consumes the charter. It reads `<artifact_root>/charter.md` in full and elicits the requirements, personas, and acceptance criteria that realise the vision and objectives the charter fixes. The requirements must serve the charter's objectives, stay inside its constraints, and be measurable against its success metrics. The charter's next steps section points into phase 1.
