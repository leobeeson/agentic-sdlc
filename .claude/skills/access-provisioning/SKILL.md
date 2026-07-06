---
name: access-provisioning
description: |
  Onboarding guide for AI-related access. Load when a developer has just joined the team or
  the company and needs accounts, model and gateway access, permissions, tools, or
  frameworks. A guided conversation that produces a step-by-step access guide with the right
  links, so the developer is never left guessing where to start. Run once per engineer.
allowed-tools: Read, Grep, Glob, Bash, WebFetch
inputs:
  - name: developer_profile
    required: true
    signal: who the developer is and the role they are joining, which determines the baseline set of access they should hold
    source: the developer's stated need, bound by the orchestrator at intake
  - name: access_needs
    required: false
    signal: any specific accounts, model or gateway access, permissions, tools, or frameworks the developer already knows they need beyond the role baseline
    source: the developer's stated need, bound by the orchestrator at intake
  - name: access_catalogue
    required: false
    signal: the team's current map of AI-related access points, request routes, and links that the guided list is built from
    source: a static reference file under ai_docs/reference/ (maintained by hand in Phase 1)
outputs:
  - type: access-provisioning guide (a step-by-step list of what to request, how, and where, with the right links)
    location: ai_docs/initiatives/<initiative-id>/access-guide.md (the initiative workspace)
preconditions: none beyond a stated onboarding need; this agent is an entry-side operational guide and does not require any prior generation, plan, or run artefact to exist
intents:
  - AI access provisioning (new-developer onboarding for AI-related access)
scope: core
model_floor: mid
cost_tier: light
standalone: yes
idempotency: reuse an existing valid guide for the same developer and role; run once per engineer, refreshing only when the role or the access catalogue changes
primitive: skill
phase: phase-1 for the guided form; phase-2 for the automated form that submits permitted requests
---

# Access Provisioning

The onboarding conversation for AI-related access. A developer who has just joined needs accounts, model and gateway access, permissions, tools, and frameworks, and rarely knows where to start. This skill walks the developer through what to request, how, and where, and leaves behind a durable guide the developer works down over the following days. The conversation runs wherever the harness is installed: an engineer with no project yet runs it from a fresh installation in an empty folder, and the guide lands in that installation's initiative workspace, because the guide is the engineer's own onboarding record, never project state.

Phase 1 is guided only: the right links and the step-by-step list. In Phase 2 this skill additionally executes the steps the enterprise permits to be automated, such as submitting a request or filling a form through an API on the developer's behalf, inside the same conversation.

## Idempotency, checked first

Look for an existing guide in the initiative workspace. A valid guide for the same developer and role is reused: present it, ask what has changed, and update only the affected items. A fresh guide is warranted only when the role or the access catalogue has changed.

## The conversation

1. **Establish the profile.** Who the developer is, the role they are joining, and their start date. The role determines the baseline access set.
2. **Read the access catalogue** at `ai_docs/reference/access-catalogue.md` when present: the team's map of access points, request routes, approvers, typical waits, and links.

   ### If the access catalogue is absent

   Do not stop and do not ask for a file. Build the guide from the developer's own knowledge elicited in conversation, the harness's defaults (the coding agent itself, the model or gateway account it needs, the repository access the pipelines assume, the warehouse access route data-engineering work depends on), and anything discoverable from the installation. Add a flagged section to the guide, directly after the provenance header:

   ```md
   ## Degraded inputs

   - access_catalogue: absent. This guide was built from the conversation and the
     harness defaults; request routes and links need confirmation by the team, and
     the team should record a catalogue at ai_docs/reference/access-catalogue.md.
   ```

3. **Establish what already exists.** Walk the baseline set and mark what the developer already holds, with the verification for each (a command that succeeds, a page that opens).
4. **Elicit the extras.** Any access the developer already knows they need beyond the baseline.
5. **Order the requests.** Sequence by dependency (an account before the permission that attaches to it) and by wait time (fire the long waits first). The longest-wait item goes first; for a data engineer that is typically the warehouse access route.

## Generate the guide

Write `ai_docs/initiatives/<initiative-id>/access-guide.md` matching `.claude/templates/access-guide.md`: what the developer already has, then each request in order, with what it is, why the role needs it, the exact request route, the link, the typical wait, and what blocks on what; then the per-item verification steps for after access lands; then open questions routed to named owners. Fill the provenance header, with a back-reference to the access catalogue when one was read.

Present the guide in the conversation as well as writing it: the developer acts on it immediately.

## Guidelines

### Do

- Fire the longest-wait requests first, and say which those are.
- Give every item a verification step, so the developer knows when access has actually landed.
- Flag every route or link the catalogue could not confirm.
- Keep the guide the developer's record: personal, dated, and self-contained.

### Do not

- Submit any request on the developer's behalf in Phase 1; the skill guides, the developer acts.
- Guess an approver or a route the catalogue does not record; flag it as an open question with an owner instead.
- Treat the guide as project state; it lives in the initiative workspace as the engineer's onboarding record.
