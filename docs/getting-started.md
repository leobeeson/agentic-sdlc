# Getting started

This guide installs the harness into a target repository, runs setup, and drives the first run. The harness ships as a project-agnostic spine: every project-specific fact lives in `sdlc.config.yaml`, generated once at setup, and the spine is never edited per project.

## Prerequisites

- Claude Code, which discovers and runs the agents and skills.
- uv, which runs the Python scripts. Each script declares its dependencies inline, so `uv run` resolves them with no separate install step.

## Step 1: Install

From the harness repository, copy the harness into your target repository:

```bash
./install.sh /path/to/target-repo
```

This copies `.claude/` (agents, skills, scripts, hooks, config, templates) and the thin `CLAUDE.md` core into the target repository root. After this step the harness lives entirely inside the target repository; nothing is shared from the harness repository at runtime.

## Step 2: Restart the session

Open Claude Code in the target repository, or restart the session if one was already open. Claude Code discovers agents and skills from `.claude/` at session start, so a restart is required before the skills below are available.

## Step 3: Run setup

```txt
/setup
```

Setup runs once and does three things:

- Writes `sdlc.config.yaml`. On a greenfield project, setup interviews you for the facts the file needs. On an existing project, the main agent surveys the repository itself (the dbt project file, the DAG configuration directory, the test layout, the base branch), drafts the file from what the survey finds, and interviews you only for what the survey cannot determine; you confirm the draft before the file is written.
- Scaffolds the project spine via `uv run .claude/scripts/scaffold.py init`: the `ai_docs/` tree with `reference/`, `initiatives/`, and the spine singletons.
- Generates the agent registry via `uv run .claude/scripts/generate_agent_registry.py`, the catalogue the orchestrator discovers agent roles from.

## Step 4: State an intent

The default way to drive the harness is to say what you need in plain language:

```txt
I need a dbt model that aggregates daily order totals per customer for the exports feed.
```

The main agent, as the concierge, classifies the intent on target and magnitude, asking only when open readings would compose materially different runs. As the orchestrator, it then selects the recipe for that pair, prunes it, states the plan with a rationale per stage, and runs it, pausing at the gates for your approval. Include the phrase `elicit first` in the intent message when you want the concierge to ask about every point it would otherwise settle by inference.

## A worked first run

Intent: the dbt request above, classified as `dbt-model` at `new-feature` magnitude. The orchestrator composes:

- Included: requirements update, implementation plan, then per task explore, prepare, generate, classify risk, review with the risk-scoped subset, consolidate, walk through, reconcile, and the run record throughout.
- Pruned by magnitude: the project charter and the architecture stage, because a new feature within the existing design records no new architectural decision.
- Skipped by idempotency: the warehouse-schema grounding, when `ai_docs/reference/schema-snapshot.md` already exists, validates, and covers the sources the spec names.

What lands where, for initiative `INIT-001-daily-order-totals` and task `TASK-001`:

```txt
ai_docs/
  prd.md                                          updated requirement
  reference/schema-snapshot.md                    grounding (reused or refreshed)
  initiatives/
    index.md                                      status sentence + focus note
    INIT-001-daily-order-totals/
      implementation-plan.md
      specs/index.md                              task registry
      specs/01-daily-order-totals.md              per-task spec
      explorations/TASK-001.md
      task-briefs/TASK-001.md
      reviews/TASK-001/                           risk classification, one review per dimension, consolidated.md
      walkthroughs/TASK-001.md
      reconciliations/TASK-001.md
      run-record/
```

The generated model and its schema file land in the application repository at the dbt location `sdlc.config.yaml` records, never inside `ai_docs/`.

## Driving by hand

Pattern B gives you control of every step. Invoke a skill directly and inspect its artefact before deciding what to run next:

- `/project-charter`, `/requirements-navigator`, `/arch-blueprint`, `/implementation-planner`: the four gated consultations.
- `/adhoc-code-implement-loop`: the per-task implementation loop for ad-hoc code.
- `/prime`: rebuild context from the artefact bus at any checkpoint.

Subagent roles are invoked by asking the main agent in plain language, for example `Run the feature-explorer for TASK-003 at thorough depth` or `Run the review panel on branch feature/exports`. Every invocation reads its inputs from the artefact bus, so rehydration comes from the artefacts, not from the conversation.

## Tracking progress

- `ai_docs/initiatives/index.md` lists every initiative with a status sentence and carries the focus note.
- Each initiative's `run-record/` says which stages ran, which were pruned or reused, and why.
- Each initiative's `specs/index.md` is its task registry.

## Troubleshooting

Validate the configuration and the spine at any time:

```bash
uv run .claude/scripts/scaffold.py validate --root .
```

The command validates `sdlc.config.yaml` against the profile model (including the rule that mandatory agent roles cannot be disabled), checks the spine is complete, and prints a JSON report. Regenerate the agent registry after adding or editing any agent or skill file:

```bash
uv run .claude/scripts/generate_agent_registry.py
```
