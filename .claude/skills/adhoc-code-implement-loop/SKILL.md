---
name: adhoc-code-implement-loop
description: |
  Implements a single task in general code from a per-task spec, with the developer driving
  step by step in the conversation. Load when the classified target is ad-hoc code
  development and a spec for the task is present: this is the generation stage of the
  ad-hoc-code recipes, performed by the main agent itself. Runs the capped testing loop and
  marks the task complete in the task registry.
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
inputs:
  - name: spec
    required: true
    signal: the self-contained per-task specification the agent implements against and verifies its work by
    source: the per-task spec in the initiative workspace, specs/
  - name: task_brief
    required: false
    signal: the distilled, self-contained work order prepared from the spec and the exploration
    source: the task brief produced by the task-preparer in the initiative workspace
  - name: exploration_report
    required: false
    signal: the breadth-and-depth map of the codebase that orients the change
    source: the exploration report produced by the feature-explorer in the initiative workspace
  - name: context
    required: false
    signal: the project vocabulary, testing conventions, and in-repo precedent the code should respect
    source: ai_docs/reference/ in the project spine (CONTEXT.md, the ubiquitous language, the testing conventions)
outputs:
  - type: implemented code and tests in the application repository, with the task marked complete in the task registry
    location: the application repository, with the run reflected in the run record and the task registry (specs/index.md) in the initiative workspace
preconditions: a per-task spec exists; the task brief and exploration report sharpen the loop when present
intents: ad-hoc code development
scope: core
model_floor: mid
cost_tier: heavy
standalone: yes
idempotency: if the task is already marked complete in the task registry and its code is present, reuse rather than re-implement
primitive: skill
phase: phase-1
---

# Ad-hoc Code Implement Loop

The generation stage for the ad-hoc-code target: one stage of the pipeline, performed by the main agent in the conversation, with the developer driving step by step. Everything around this stage (exploration, preparation, review, consolidation, walkthrough, reconciliation, the run record) belongs to other stages the orchestration skill sequences; this skill implements exactly one task and proves the implementation against the task's own validation commands.

## Idempotency, checked first

Read the task registry at `ai_docs/initiatives/<initiative-id>/specs/index.md`. When the task is already marked complete and its code is present in the repository, reuse: state that fact and stop, unless the developer explicitly asks for re-implementation.

## The higher-order prompt

The per-task spec is the prompt. A per-task specification is engineering compressed into natural language: at once a durable artefact on the artefact bus and the instruction this stage executes. Whatever planning stage produced the spec, this one consumer runs it, which keeps planning and implementation decoupled across the artefact bus.

```md
# Implement the plan

Follow the `Instructions` to implement the `Plan`, then produce the `Report`.

## Instructions
- Read the plan, think hard about the plan, and implement the plan.

## Plan
<the per-task spec>

## Report
- Summarise the completed work as a concise bullet list.
- Report the files and total lines changed with `git diff --stat`.
```

## Read the context, in order

1. The per-task spec at `ai_docs/initiatives/<initiative-id>/specs/<task-id>.md`: the work order and the validation commands.
2. The task brief at `task-briefs/<task-id>.md` in the initiative workspace, when present: the distilled requirements, the test plan, the code hints, and the flagged checkpoints.
3. The exploration report at `explorations/<task-id>.md`, when present: the integration points, the patterns to follow, and the complications.
4. `ai_docs/reference/CONTEXT.md` and `ai_docs/reference/testing-conventions.md`: the vocabulary every name must use, and the testing cadence.

### If the task brief is absent

Do not stop and do not ask. Implement from the spec, the reference documents, and your own reading of the code the spec names. State once, in the conversation, that the brief was absent and the implementation proceeded from the spec alone.

### If the exploration report is absent

Proceed from the spec and the brief, and lean harder on the side-quest rule below: what the exploration would have pre-answered, the feature-explorer answers on demand.

## Implement with TDD vertical slices

Work the spec's steps in order, one behaviour at a time, following the test plan when a brief carries one:

1. Write one test for the next behaviour (RED: the test must fail).
2. Write the minimal code that makes it pass (GREEN: no more code than needed).
3. Repeat for the next behaviour.
4. Refactor once all behaviours are green (REFACTOR: extract, simplify, clean up).

Rules that hold throughout:

- Never write all tests first, then all code; each test responds to what the previous cycle taught.
- Never refactor while RED; reach GREEN first.
- Tests verify behaviour through public interfaces, never implementation details; a test that breaks on an internal rename was testing implementation.
- Mock only at system boundaries (model calls, databases, external HTTP, time and randomness); never mock internal classes you wrote.
- Test names describe what the system does, not how.

## The side-quest rule

During implementation, questions arise that need investigation: how another module handles something, what an API contract looks like, how a library is used elsewhere. When answering would mean reading five or more files, or researching an unfamiliar library or API, spawn the feature-explorer in ad-hoc mode instead of investigating inline. The explorer runs in a fresh context and returns a focused answer with evidence, and this conversation stays clean of raw research. Use the rule liberally.

## The material-impact escalation rule

Stop and put the question to the developer at any point of genuine ambiguity: an architectural choice the spec and the reference documents do not cover, a contradiction between the spec and the code, or any point where proceeding on an assumption could waste significant work if the assumption is wrong. A question with material impact on the intent is never settled by assumption. The developer is present, because this stage runs in the conversation; ask directly, record the decision where it meets the ADR bar (hard to reverse, surprising without context, a real trade-off), and continue.

## Code standards

Every line will be read by the reviewers and by colleagues. The code must be:

- **Correct.** Robust error handling at every boundary; no silent failures, no swallowed exceptions, no defensive code against impossible states.
- **Tested.** Every behaviour in the test plan has a passing test, following the recorded testing conventions.
- **Lean.** No speculative features, no unnecessary abstraction, no commented-out code; every line earns its place.
- **Readable.** Clear names in CONTEXT.md vocabulary, small functions, obvious control flow.
- **Evolvable.** Designed for the next task to build on.
- **Secure.** No secrets in code; input validation at boundaries; authentication and authorisation checks where required.

## The capped testing loop

Close the stage with the testing loop, run against the spec's Validation Commands:

1. **Run the validators**: every command in the spec's Validation Commands section, verbatim.
2. **Parse the failures** into a list.
3. **Fix each failure** on the list.
4. **Re-run** every validator, because a fix can break another check.

The loop stops on exactly one of three conditions: zero failures (success); the retry cap of three iterations, after which the remaining failures are put to the developer plainly rather than iterated further; or zero progress, an iteration that fixed nothing, which stops the loop early because iteration without progress spends tokens and changes nothing. Never weaken a test to make it pass: when a test is wrong, change the test deliberately and say so.

## Close the task

When the validators pass and the developer is satisfied:

- Produce the Report: the concise bullet summary and `git diff --stat`.
- Mark the task complete in the task registry at `specs/index.md` in the initiative workspace.
- The run record and the downstream stages (risk classification, review, consolidation, walkthrough, reconciliation) belong to the orchestration skill, which continues the composed plan from here.

No completion summary is returned: the main agent performed this stage itself, and the conversation already holds everything a summary would carry.

## Guidelines

### Do

- Execute the spec's steps in order, top to bottom, finishing with the Validation Commands.
- Keep slices vertical and behaviours singular; one RED/GREEN cycle per behaviour.
- Spawn the feature-explorer for any five-file question or unfamiliar dependency.
- Stop on material ambiguity and ask; the developer is in the conversation.
- Cap the testing loop and report residual failures honestly.

### Do not

- Re-implement a task the registry already marks complete, unless explicitly asked.
- Settle a material point by assumption.
- Mock internals, test implementation details, or write all tests up front.
- Weaken a failing test to reach green.
- Run the downstream stages from here; the orchestration skill owns the sequence.
