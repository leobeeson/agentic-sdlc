<!-- TEMPLATE: the developer runbook, the operator reference for driving the
     agentic SDLC harness on this project. Placed into the artefact tree at
     setup at ai_docs/runbook.md and kept current by hand. -->

<!-- PROVENANCE (append-only; only created is fixed) -->
created:        <ISO-8601 timestamp>
modified:       [<ISO-8601 timestamp>]
commits:        [<short-sha>]
agents:         [setup]
run-ids:        [<run-id>]
back-refs:      [sdlc.config.yaml]
forward-refs:   [none]
<!-- END PROVENANCE -->

# Runbook

How to drive the agentic SDLC harness on this project.

## Setup, once

- Run the `setup` skill after the harness is copied in. It scaffolds the two-tier artefact tree (`uv run .claude/scripts/scaffold.py init --root .`), then writes `sdlc.config.yaml` by greenfield interview or brownfield survey, and generates the agent registry (`uv run .claude/scripts/generate_agent_registry.py`).
- Validate at any time with `uv run .claude/scripts/scaffold.py validate --root .`.

## Pattern A: orchestrator-driven (the default)

State what you need in plain language. The main agent classifies the intent
(target and magnitude), composes a pruned execution plan from the matching
recipe, runs it, and pauses at the gates for your approval. Read the run record
under `ai_docs/initiatives/<initiative-id>/run-record/` to see which stages ran
and why.

- To force a full question-and-answer intake instead of inference, include the phrase `elicit first` in the message that states the intent.
- To rebuild an existing artefact, ask for it to be regenerated; the orchestrator treats the artefact as absent and overwrites it in place, and the provenance header keeps the lineage.

## Pattern B: hand-driven checkpoints (power users)

Advance one agent role at a time and inspect each artefact before deciding what
runs next.

- Skill-realised roles are invoked directly: `/project-charter`, `/requirements-navigator`, `/arch-blueprint`, `/implementation-planner`, `/adhoc-code-implement-loop`, `/access-provisioning`, plus `/prime` for the context rebuild.
- Subagent-realised roles are invoked by asking the main agent, for example: "Run the feature-explorer for TASK-003 in preparation mode at medium depth", or "Run the review panel on branch feature/orders-dedup".
- Every invocation is the standalone binding: the agent role reads its declared inputs from the artefact bus, or from what you supply directly (a file, a path, a dictated paragraph).

## Session hygiene

After a consultation ends and its artefact is confirmed onto the artefact bus,
clear the session with `/clear`. The fresh session's concierge proposes the
focus-note initiative from the initiative registry, you confirm, the prime
skill reloads only the run record and the artefacts the next stage needs, and
the next stage starts on a small, rebuilt context instead of on top of the
whole consultation exchange. Use the same reset after a generation stage or
after the reviews. A session cannot clear itself: proposing the reset is the
orchestrator's duty, performing it is yours.

## Reviews on work the pipeline never saw

A branch or pull-request review needs no upstream artefacts: "Review branch
<name>" runs the risk-classifier, the recommended reviewer subset, and the
consolidator, and returns one evidence-traced verdict.
