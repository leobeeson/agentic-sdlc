---
name: intake
description: |
  Harness-core skill carrying the concierge procedure: the session-start protocol over the
  initiative catalogue, the confirmation of one initiative, the classification of the
  developer's stated intent on target and magnitude, the elicitation flag, the
  inline-versus-spawn investigation threshold, and the malformed-input edge cases. Load when
  a session starts or when the developer states an intent. Not a catalogue entry: the
  concierge is a role the main agent plays, immune to the availability switch.
scope: harness-core
phase: phase-1
---

# The intake skill: the concierge procedure

You are the main agent playing the concierge, the intake role. Intake is inline by default: you classify in the conversation, and nothing is spawned to classify. Your output is the detected intent, recorded in the run record; your final instruction hands over to the orchestrator role.

## 1. The session-start protocol

On a fresh session (a new startup, a session after `/clear`, or a resumed session), a SessionStart hook injects the initiative catalogue and the reconstitution protocol. When no injection arrived (the hook is not registered on this installation), build the catalogue yourself: read `ai_docs/initiatives/index.md` (the initiative registry) and, for detail on any entry, the initiative's `run-record/` directory. Then follow the protocol:

1. When the initiative catalogue is empty, because the project has no initiative yet, proceed directly to classification (section 2). Nothing is proposed and nothing is rebuilt.
2. When the focus note names one obvious continuation, open by proposing to resume that initiative, summarising its state from the catalogue entry, and invite the developer to confirm or switch.
3. Otherwise present the catalogue and ask: continue an ongoing initiative, revisit a finished initiative, or start a new intent.
4. After the developer confirms one initiative, invoke the prime skill, so the run record and the confirmed initiative's output artefacts land in context, then continue at the next stage under the orchestration skill.
5. For a new intent, run the classification below.

The focus note is a default, never a lock: the developer always confirms before anything is read, and a switch rewrites the focus note (the orchestrator's write).

## 2. Classification on two dimensions

Classify the stated intent against the two vocabularies in `.claude/config/intents.yaml`.

- The **target** names the kind of work and selects the recipe family. The eight targets are a closed enumeration; a target outside the list cannot run, because no recipe binds to it.
- The **magnitude** applies only to the three generation targets and says how much of the lifecycle the work needs: bug-fix, feature-update, new-feature, new-capability, new-project, each defined by what the intent does to the product, never by how many lines it touches. The other five targets carry no magnitude; record none for them.

Resolution order, per label:

1. An explicit statement by the developer wins: a developer who says "this is a bug fix" has classified the magnitude, and one who says "let's talk this through" has classified the target.
2. Otherwise infer the label from the stated intent against the definitions in `intents.yaml`.
3. Ask only when the intent leaves readings open whose compositions would materially differ, and ask again when the answer leaves the material point unresolved: a point with material impact is never settled by guessing. A point without material impact is settled by inference, so intake stays short by default.

The magnitude also sets the model dial for the run, once, at classification: base for bug-fix, feature-update, and new-feature; full for new-capability and new-project (`intents.yaml`, `model_dial`). Record the dial position with the intent.

## 3. The elicitation flag

The reserved phrase `elicit first` in the message that states the intent inverts the default: ask about every point you would otherwise have settled by inference, in a structured question-and-answer session, before anything is composed. The flag exists because inference and questioning do not cost the same for every developer: a developer on unfamiliar ground may prefer ten questions over one wrong inference, and a developer who knows exactly what the work needs prefers no questions at all.

## 4. The inline-versus-spawn threshold

Classification sometimes needs investigation, because the message references files, datasets, or a term you must understand before you can classify. A small lookup stays inline. Beyond the threshold, spawn the feature-explorer instead, because an investigation that fills your context with files you will never need again defeats the purpose of the fresh-context subagent. The threshold, a proposed default tunable with usage:

- Code: about five files, or one unfamiliar library or API.
- Data: the schema or lineage of roughly five or more datasets or models, or an unfamiliar ADP Foundry operator.

## 5. Malformed and partial input

Elicit what is missing rather than rejecting what arrived:

- **An intent that fits no target.** Ask what the developer meant. A developer who only wants to talk is already served, because ad-hoc conversation is a target.
- **A reference that cannot be read.** When the message names a path that does not exist, or a resource that cannot be fetched, state exactly what you could not read and ask for the missing piece, rather than classifying around the gap.
- **A message carrying more than one intent.** Propose splitting the message into separate initiatives, state the order you would run them in, and let the developer confirm or reorder before anything is classified.

## 6. The handover

Record the detected intent, the target, the magnitude where one applies, and the dial position, in the run record of the initiative (minting is the orchestrator's job; when this is a new intent, note the classification for the orchestrator's entry step). Then load the orchestration skill. This instruction is the transition from the concierge role to the orchestrator role: the concierge is the orchestrator, one agent closing one procedure and loading the next.
