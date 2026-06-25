# Getting Started

This guide walks you through adopting the agentic SDLC framework in a target repository. You bootstrap the framework into the repository, let Claude Code discover the new agents and skills, run setup, and then drive the pipeline phase by phase.

The framework ships as a project-agnostic spine. Every project-specific fact lives in a single configuration file, `sdlc.config.yaml`, generated once at setup and read in slices by every agent. The spine is never edited per project, and nothing is shared from the framework repository at runtime: everything lives visibly inside your own repository.

## Prerequisites

- Claude Code, which discovers and runs the agents, skills, and commands.
- uv, which runs the Python scaffolding CLI. The scaffolding script declares its own dependencies inline, so `uv run` resolves them with no separate install step.

## Step 1: Bootstrap

From the framework repository, copy the framework into your target repository, passing the target path as the only argument:

```
./install.sh /path/to/target-repo
```

This copies the framework's `.claude/` directory into the target repository root. The copied `.claude/` carries everything Claude needs: `agents/`, `skills/`, `commands/`, `scripts/` (the Python CLIs the agents call), `config/` (the profile schema and examples), and `templates/` (the format templates placed into the artifact tree). A single copy brings the whole system across.

After this step, the framework lives entirely inside the target repository. Nothing is shared from the framework repository at runtime, and nothing hides in a user home directory. You own the copy and can read every agent, skill, command, and script inside your own project.

## Step 2: Discover

Open Claude Code in the target repository. If a session was already open in that repository, restart it.

Claude Code discovers agents, skills, and commands from the target's `.claude/` at session start. A restart is required for the newly copied agents and skills to register; without it, the commands in the following steps will not be available.

## Step 3: Setup

Run the setup skill:

```
/setup
```

The setup skill runs once, immediately after the framework has been copied in, and leaves the repository ready for phase 0. It does two things:

- Creates the complete, documented artifact tree under the configured `artifact_root` via the scaffolding CLI. Every directory is present, each with a README and the format template for its artifacts, so you see the full structure up front.
- Writes `sdlc.config.yaml` at the repository root, the single source of every project-specific fact. Greenfield projects are set up by interview, where the skill asks you for the facts the profile needs. Brownfield projects are set up by a scan of the existing codebase via the `profile-discoverer` agent, which drafts the profile from evidence (language, package manager, test runner, CI files, deploy configuration, directory conventions) for you to confirm.

The skill is the seam: the agent gathers and confirms the configuration and verifies the end state, while the CLI guarantees the scaffolding is exact and repeatable. Setup finishes by validating the result, so you start the pipeline from a known-good state.

## Step 4: Drive the pipeline

The pipeline has two halves. The front half (phases 0 to 3) is interactive: the skills converse with you to elicit the charter, requirements, architecture, and plan. The back half (phase 4) is headless: an orchestration skill drives subagents that run in fresh context, report evidence, and never converse.

Drive the phases in order:

- `/initialise-project` writes `charter.md`: the vision, objectives, success metrics, constraints, stakeholders, and risks.
- `/define-requirements` reads the charter and writes `prd.md`: requirement identifiers with MoSCoW priority, user personas, and acceptance criteria in a Given/When/Then grammar.
- `/design-architecture` reads the requirements and writes `architecture.md`, diagrams, and architectural decision records under `reference/adr/`.
- `/plan-implementation` reads the architecture and requirements and writes `implementation-plan.md`, the spec documents under `specs/`, and the task registry `specs/index.md`. This phase is the join: it emits exactly what the implementation loop consumes.

Then, for each task in the registry, run the per-task loop:

```
/implement-task <task-id>
```

For example, `/implement-task TASK-001`. The loop runs, in order: explore, prepare, implement, review panel, consolidate, walkthrough, and reconcile. The reconcile stage updates the spec document in place so it reflects what was actually built. Run `implement-task` once per task, working through the registry.

## Where artifacts land

All artifacts live under one tree, the configured `artifact_root`. The default is `ai_docs`.

```
ai_docs/
  charter.md                  Phase 0 output
  prd.md                      Phase 1 output
  architecture.md             Phase 2 output
  implementation-plan.md      Phase 3 output
  diagrams/                   Phase 2 diagrams
  specs/
    index.md                  Task registry: task to spec map and status board
    NN-<area>.md              Per-area spec documents, contain tasks
  reference/                  Living project-state documents
    CONTEXT.md                Domain glossary, ubiquitous language
    testing-conventions.md    Testing patterns and cadence
    adr/                      Architectural decision records
    <domain>.md               One per concern, created as needed
  task-briefs/
    <task-id>.md              Per-task brief
  explorations/
    <task-id>.md              Per-task exploration
  reviews/
    <task-id>/
      <dimension>.md          One per reviewer in the roster
      consolidated.md         The authoritative consolidated verdict
  walkthroughs/
    <task-id>.md              Per-task walkthrough
  reconciliations/
    <task-id>.md              Per-task reconciliation
  runbook.md                  How to run the phases
```

## How to track progress

The pipeline is completely self-contained. There is no synchronisation to any external tracker.

- `specs/index.md` is the task registry and status board. It maps each task id to its spec document and records the status of every task.
- The per-task artifacts under the artifact tree are the rest of the system of record.

To check progress, read `specs/index.md`. To trace what happened on a given task, read its exploration, brief, reviews, walkthrough, and reconciliation.

## The review panel

Code review is a standard stage of `implement-task`, not an optional side call. The review panel runs automatically inside the per-task loop: a roster of reviewers, each spawned with one dimension and run in parallel, followed by a consolidator that writes the authoritative verdict.

You can also run the panel standalone against a task:

```
/review <task-id>
```

The default roster is the nine dimensions in the profile: spec-conformance, correctness, state-and-concurrency, security-and-trust-boundary, failure-and-robustness, observability, test-adequacy, interface-and-data-integrity, and conventions. A profile flag picks light mode (a subset of reviewers) or thorough mode (the full roster).

## Troubleshooting

If anything looks wrong, validate the configuration and the artifact tree at any time:

```
uv run .claude/scripts/scaffold.py validate --root .
```

This validates `sdlc.config.yaml` against the profile model, checks the artifact tree is complete, and prints a JSON report. If `valid` is false, read the `errors` and `missing_paths`. A malformed or incomplete config is fixed by editing `sdlc.config.yaml`; a missing tree path is restored by re-running the init command from the setup skill. Validate again until it reports valid.
