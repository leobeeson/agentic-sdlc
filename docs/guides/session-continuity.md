# Session continuity

This guide explains how an initiative survives sessions: why the harness does not rely on compaction, what a fresh session receives, how the right initiative is confirmed, and how the prime skill rebuilds context from the artefact bus.

## Why compaction is not relied on

The consultations run inside the main agent's session, so each consultation's whole exchange accumulates in the context window the orchestrator uses, and an initiative also outlives a session: a developer closes the terminal at the end of the day, or an initiative blocks on an external dependency while the developer moves to another. Claude Code's built-in answer to a long conversation is compaction, which replaces the conversation with a summary, and a summary drops detail that nobody chose to drop. The harness does not rely on compaction, because everything the orchestrator needs is already durable on the artefact bus: the run record carries the detected intent, the composed plan, the rationale per stage, and the outcome per stage, and the output artefacts are the durable products of every completed stage. A fresh session therefore rebuilds losslessly from files, and the cost of a rebuilt session scales with one initiative's artefacts rather than with the length of the accumulated conversation.

## What a fresh session receives

Every fresh session (a new startup, a session after `/clear`, or a resumed session) fires the SessionStart hook `.claude/hooks/build_initiative_catalogue.py`, registered in `.claude/settings.json`. The hook is code and holds no judgement: it reads the initiative registry and the run records, builds the initiative catalogue, and injects the catalogue together with the reconstitution protocol into the new session. The catalogue holds one entry per initiative: the identifier, the intent as target and magnitude, the status sentence, the next or last stage, and how recently the initiative was touched. The hook injects no output artefact of any initiative, because the prime skill performs every artefact read after the developer confirms one initiative. The hook deliberately does not fire on compaction, because the rebuild replaces compaction rather than complementing it. When the hook is not registered on an installation, the intake skill builds the same catalogue itself by reading `ai_docs/initiatives/index.md`.

## The first turn and the focus note

On a project with no initiative yet, the catalogue is empty and the first turn is the normal intake: nothing is proposed and nothing is rebuilt. Every other fresh session faces an identification question, because several initiatives may exist and several may be unfinished at once. The focus note removes the question in the common case: it is the one line in the initiative registry recording the initiative the developer last confirmed, rewritten by the orchestrator at every confirmation. When the focus note resolves to one obvious continuation, the concierge opens by proposing to resume that initiative and invites the developer to confirm or switch; otherwise it presents the catalogue and asks. The focus note is a default and never a lock: the developer always confirms before anything is read, and a stale focus note costs one turn.

## The prime skill

After the developer confirms one initiative, the orchestrator invokes the prime skill (`.claude/skills/prime/SKILL.md`), which the developer can also invoke by hand as `/prime` at any checkpoint. One skill serves both halves of the context job:

- The grounding half loads the project's standing context: `sdlc.config.yaml`, the spine's `CONTEXT.md` and ubiquitous language, and the initiative registry.
- The rebuild half reads the confirmed initiative's run record and every output artefact the record names, plus the spine artefacts the next stage's contract declares as inputs.

The prime skill runs inline, never forked, because the whole point of the rebuild is that the artefacts land in the main agent's own context window; a forked skill would read them into a separate context and return only a summary. The conversational exchanges of earlier consultations are deliberately not carried across: each consultation's output artefact is the durable product of its conversation, and the orchestrator depends on nothing the artefact does not hold. When the rebuild finishes, the main agent states the intent, the stages completed, and the next stage, and continues there.

## The clear rule

One hygiene rule pairs with the mechanism: after a consultation ends and its artefact is confirmed onto the artefact bus, clear the session with `/clear`. A session cannot clear itself, so the clear is the developer's action, and proposing it is the orchestrator's written duty: after each skill-performed stage, and at any checkpoint where the accumulated conversation no longer serves the next stage, for example after a generation stage or after the reviews. The cleared session fires the SessionStart hook, the concierge proposes the focus-note initiative, and the next stage starts on a small, rebuilt context instead of on top of the whole consultation exchange.
