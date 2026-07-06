---
name: prime
description: |
  Harness-core skill carrying the context rebuild: loads the project grounding (the spine's
  CONTEXT.md and ubiquitous language, the project configuration, the initiative registry) and
  reads the run record and every output artefact of one confirmed initiative into the main
  agent's own context. Run inline, never forked: the whole point of the rebuild is that the
  artefacts land in the main agent's context window. Invoked by the orchestrator after the
  developer confirms an initiative, or by hand as /prime at any checkpoint.
scope: harness-core
phase: phase-1
---

# The prime skill: grounding plus rebuild

One skill serves both halves of the context job. Run every read inline, in this session; never fork, because a forked skill would read the artefacts into a separate context and return only a summary, which defeats the rebuild.

## Half 1: the project grounding

Load the project's standing context, in this order:

1. `sdlc.config.yaml`: the per-project profile, read whole (it is small by design).
2. `ai_docs/reference/CONTEXT.md` and the ubiquitous language: the recorded vocabulary every artefact uses.
3. `ai_docs/initiatives/index.md`: the initiative registry, with its status sentences and the focus note.

## Half 2: the rebuild of one confirmed initiative

After the developer has confirmed one initiative (the intake skill's session-start protocol):

1. Read the initiative's run record directory, `ai_docs/initiatives/<initiative-id>/run-record/`: the detected intent, the composed plan, the rationale per stage, and the outcome per stage.
2. Read every output artefact the run record names as produced for this initiative: the implementation plan, the specs and the task registry, the explorations, the task briefs, the reviews and the consolidated verdicts, the walkthroughs, the reconciliations, in whatever subset exists.
3. Read the spine artefacts the next stage's contract declares as inputs (for example `prd.md` and `architecture.md` before the implementation-planner; `reference/schema-snapshot.md` before dbt generation).

Do not reload the conversational exchanges of earlier consultations: each consultation's output artefact is the durable product of its conversation, and the orchestrator depends on no part of the exchange that the artefact does not already hold. The rebuild is lossless where compaction is lossy, because the rebuild reloads the durable artefacts themselves rather than a summary, and its cost scales with one initiative's artefacts rather than with the accumulated conversation.

## Closing statement

When the rebuild finishes, state the rebuilt state in three lines: the intent (target and magnitude), the stages completed, and the next stage. Then continue orchestration at that stage.

- For a finished initiative, the rebuild only reads and writes nothing, which is enough for a walkthrough or a review of the pull request without reopening the pipeline.
- For a new intent, hand off to the intake skill's classification instead.
