# Agentic SDLC: Design

## Purpose

A portable, self-contained agentic software development lifecycle pipeline. It is a set of Claude Code agents, skills, commands, and supporting Python tooling that a team copies into any project repository and then drives end to end: from project vision through requirements, architecture, planning, implementation, and code review.

The intent is ad-hoc spec-driven development that works the same way in any repository, with no per-project changes to the pipeline itself.

## Design thesis

One decision governs the whole system: the pipeline ships as a project-agnostic spine, and every project-specific fact lives in a single per-project configuration file, `sdlc.config.yaml`, generated once at setup and read in slices by every agent thereafter. The spine (the agents, skills, commands, and scripts) is never edited per project. This pattern separates a stack-agnostic spine from a swappable per-repo profile across the entire pipeline.

Three consolidations follow from the thesis:

1. One artifact root, configurable, default `ai_docs/`. All pipeline artifacts live under one tree.
2. No external trackers. The pipeline is completely self-contained and tracker-agnostic. All tracking lives inside the artifact tree as files. There is no synchronisation to any external tracker or system. The task registry and the per-task artifacts are the system of record.
3. All coupling moves to `sdlc.config.yaml`. Hardcoded story prefixes, branch names, test commands, audit paths, and tracker sync are replaced by configuration fields and a generated task registry.

## Core concepts and vocabulary

- **Task.** The unit of work in the implementation phase. Flat, single global sequence (`TASK-001`, `TASK-002`). There is no epic or story hierarchy inside the pipeline. Epic and story are product-planning language and stay in the requirements phase. A task is the thing that flows through explore, prepare, implement, review, walkthrough, and reconcile.
- **Spec document.** A markdown document under `specs/`, one file per area of concern (`specs/NN-<area>.md`). Spec documents group tasks for readability. The grouping is file organisation only, not a formal hierarchy level. Specs are living documents: after a task is implemented and reviewed, the spec-reconciler updates the spec in place so it always reflects the reality of what was built, not just what was originally intended.
- **Task registry.** `specs/index.md`. The map from task id to its spec document, plus the status board for every task. This replaces any external tracker.
- **Profile.** `sdlc.config.yaml` at the target repository root. Holds every project-specific fact: tech stack, test commands, base branch, conventions, review roster, failure-pattern idioms.
- **Artifact.** Any file the pipeline produces under the artifact root: charter, requirements document, architecture document, implementation plan, spec documents, task briefs, explorations, reviews, walkthroughs, reconciliations, reference docs, decision records.

## The SDLC phase model

The pipeline has two halves with different interaction models.

The front half (phases 0 to 3) is interactive. The skills converse with the developer to elicit charter, requirements, architecture, and plan. They run in the main context and may spawn research subagents.

The back half (phase 4) is headless. An orchestration skill drives subagents that run in fresh context, report evidence, and never converse.

### Phase 0: Initialise

- Skill: `initialise-project`.
- Produces: `charter.md` (vision, objectives, success metrics, constraints, stakeholders, risks).
- Note: the profile (`sdlc.config.yaml`) is produced earlier, by the setup skill, because every agent including this one reads it. The profile is how the project is built; the charter is what and why it is built.

### Phase 1: Requirements

- Skill: `define-requirements`.
- Reads: `charter.md`.
- Produces: `prd.md` with requirement identifiers and MoSCoW priority, user personas, and acceptance criteria in a Given/When/Then grammar.
- May spawn: `requirements-analyst` subagents to fan out persona drafting, functional-requirement extraction, and edge-case enumeration in parallel, then merge.

### Phase 2: Architecture

- Skill: `design-architecture`.
- Reads: `prd.md`.
- Produces: `architecture.md`, diagrams under `diagrams/`, seeds for `reference/CONTEXT.md` and domain reference docs, and architectural decision records under `reference/adr/`.
- May spawn: `architecture-advisor` subagents to evaluate trade-offs (synchronous versus asynchronous, storage options, integration patterns) in parallel.

### Phase 3: Plan (the join)

- Skill: `plan-implementation`.
- Reads: `architecture.md` and `prd.md`.
- Produces: `implementation-plan.md`, the spec documents `specs/NN-<area>.md`, and the task registry `specs/index.md`.
- May spawn: `plan-decomposer` subagents to decompose work into tasks and write the spec documents.
- This phase is the join into the implementation loop. It emits exactly what the loop consumes: spec documents and a task registry. The loop assumes these already exist and were authored elsewhere; this phase produces them.

### Phase 4: Implement

- Orchestration skill: `implement-task`.
- Runs per task, in order:
  1. **Explore** (`feature-explorer`) writes `explorations/<task-id>.md`.
  2. **Prepare** (`task-preparer`) writes `task-briefs/<task-id>.md`.
  3. **Implement** (the developer with Claude) writes code and tests.
  4. **Review panel** (one `reviewer-<dimension>` agent per dimension, in parallel) writes `reviews/<task-id>/<dimension>.md`.
  5. **Consolidate** (`review-consolidator`) writes `reviews/<task-id>/consolidated.md`.
  6. **Walkthrough** (`code-walkthrough`) writes `walkthroughs/<task-id>.md`.
  7. **Reconcile** (`spec-reconciler`) updates the spec document directly so it reflects what was actually built, updates `reference/`, and writes `reconciliations/<task-id>.md` as the audit trail of what changed and why.
- The review panel is added between implement and walkthrough; otherwise this is the standard per-task loop.

There is no separate phase 5. The adversarial review method is the shared reviewer contract, and the CI merge gate is dropped.

## The artifact tree

All artifacts live under the configurable artifact root, default `ai_docs/`. The setup skill creates the complete tree at setup time, with each directory carrying a README describing its purpose and the format template for its artifacts, so the developer has full visibility of the structure before any work starts.

```
ai_docs/
  charter.md                      Phase 0 output
  prd.md                          Phase 1 output
  architecture.md                 Phase 2 output
  implementation-plan.md          Phase 3 output
  diagrams/                       Phase 2 diagrams
  specs/
    index.md                      Task registry: task to spec map and status board
    NN-<area>.md                  Per-area spec documents, contain tasks
  reference/                      Living project-state documents
    CONTEXT.md                    Domain glossary, ubiquitous language
    testing-conventions.md        Testing patterns and cadence
    adr/                          Architectural decision records
    <domain>.md                   One per concern, created as needed
  task-briefs/
    <task-id>.md                  Per-task brief (task-preparer)
  explorations/
    <task-id>.md                  Per-task exploration (feature-explorer)
  reviews/
    <task-id>/
      <dimension>.md              One per reviewer in the roster
      consolidated.md             The authoritative consolidated verdict
  walkthroughs/
    <task-id>.md                  Per-task walkthrough (code-walkthrough)
  reconciliations/
    <task-id>.md                  Per-task reconciliation (spec-reconciler)
  runbook.md                      How to run phases, generalised from the codex runbook
```

Decisions captured in this tree:

- Architectural decision records live in `reference/adr/`, not `reference/decisions/` and not a top-level `adr/`.
- A separate `validations/` directory is not used. Validation output lives under `reviews/`, where the spec-conformance reviewer covers it.
- A separate per-spec verifications location is not used. Everything is unified under one artifact root.

## The project profile

`sdlc.config.yaml` at the target repository root is the single source of project coupling. Every agent reads its slice. The schema shape (finalised during build):

```yaml
project:
  name: string
  description: string
  kind: greenfield | brownfield

artifact_root: ai_docs

task:
  id_scheme: "TASK-{NNN}"
  spec_grouping: by-concern

vcs:
  default_base_branch: master
  branch_scheme: "feature/{task-id-lower}-{slug}"

tech_stack:
  language: python
  package_manager: uv
  # further fields detected at setup or supplied by interview

test_gate:
  commands:
    - "uv run pytest -q"
  conventions_doc: reference/testing-conventions.md
  test_naming: "test_{behaviour}"

deploy_config:
  detected: false
  config_files: []
  # populated only for projects with a deployment surface

reference:
  context_doc: reference/CONTEXT.md
  adr_dir: reference/adr

review:
  mode: thorough | light
  roster:
    - spec-conformance
    - correctness
    - state-and-concurrency
    - security-and-trust-boundary
    - failure-and-robustness
    - observability
    - test-adequacy
    - interface-and-data-integrity
    - conventions
  consolidator: review-consolidator
  severity_model: "irreversibility x silence x blast-radius"

failure_patterns:
  state_consistency: []
  trust_boundary: []
  observability: []
  robustness: []
  live_path_wiring: []

subsystem_index:
  enabled: false
  path: null
```

The profile replaces these hardcoded couplings:

- The task-preparer's hardcoded prefix to spec mapping becomes `task.id_scheme` plus the generated `specs/index.md` registry.
- The validator's hardcoded base branch and `python -m pytest tests/` become `vcs.default_base_branch` and `test_gate.commands`.
- The auditor's hardcoded audit-required path prefixes are dropped with the CI gate.
- The reconciler's external tracker sync is dropped entirely.
- A subsystem index becomes the optional `subsystem_index`, off by default, degrading gracefully when absent.

## Agents

All agents are Claude Code subagents, `model: opus`, defined under `.claude/agents/`.

New agents:

- **profile-discoverer.** Scans an existing repository to draft `sdlc.config.yaml` from evidence (language, test runner, CI files, deploy config, directory conventions, idioms), for the developer to confirm. The brownfield path of setup.
- **requirements-analyst.** Fan-out research and drafting for phase 1 (personas, functional requirements, edge cases).
- **architecture-advisor.** Trade-off analysis for phase 2.
- **plan-decomposer.** Decomposes the plan into tasks and writes the spec documents in phase 3.
- **reviewers/ (nine agents).** One dedicated agent per review dimension (`reviewer-spec-conformance`, `reviewer-correctness`, and so on), under `.claude/agents/reviewers/`. Each is read-only and fully self-contained: it carries the complete adversarial review doctrine (code and deployed configuration are the only source of truth, the diff is the trigger and prime suspect but never the search boundary, no finding asserted without a trace to the actual file and line, severity ranked by irreversibility times silence times blast radius) plus a deep section for its single dimension. The profile `review.roster` selects which run.
- **review-consolidator.** Reads every reviewer's findings, deduplicates overlaps, resolves disagreements, re-validates each surviving finding against the actual code to kill false positives, ranks by severity, and writes the consolidated verdict.

The implementation-loop agents:

- **feature-explorer.** Read-only investigator. Reads the spec, `reference/CONTEXT.md`, `reference/testing-conventions.md`, the codebase, other repos, and online docs. Writes `explorations/<task-id>.md` in preparation mode, or returns findings directly in ad-hoc mode.
- **task-preparer.** Reads the spec, the exploration, and reference docs. Writes `task-briefs/<task-id>.md`. The hardcoded prefix to spec mapping is replaced by a lookup in `specs/index.md`.
- **code-walkthrough.** Reads the task brief, exploration, consolidated review, and `reference/`. Writes an execution-flow-ordered `walkthroughs/<task-id>.md` for the developer to audit before merge.
- **spec-reconciler.** Reads the consolidated review and the spec, taking the implementation as ground truth. Updates the spec document directly so it reflects what was actually built, updates `reference/` and `reference/adr/`, and writes `reconciliations/<task-id>.md` as the audit trail. An earlier version only proposed spec changes for human review, because an external tracker sync required a human to propagate them. That sync is dropped, so the reason for proposal-only is gone: the spec is a purely local file, the implementation is the source of truth, and the spec is mutated in place to match. The reconciliation report records every change so it remains reviewable.

Folded in, not standalone:

- The **feature-validator** behaviour becomes the `reviewer-spec-conformance` agent.
- The adversarial review doctrine (one dimension per reviewer, code as the only source of truth, no assert without trace) is the shared contract carried by every reviewer agent, with dedicated agents for the state-and-concurrency, security-and-trust-boundary, failure-and-robustness, and observability dimensions, alongside `review-consolidator`.

## Skills

All skills are defined under `.claude/skills/`.

- **setup.** The single setup entry point. Agent-driven over a Python CLI. Creates the artifact tree and writes `sdlc.config.yaml` (greenfield interview or brownfield scan). See Distribution and setup.
- **sdlc.** The umbrella skill: the phase map and orchestration spine, the index of the whole pipeline.
- **initialise-project.** Phase 0.
- **define-requirements.** Phase 1.
- **design-architecture.** Phase 2.
- **plan-implementation.** Phase 3.
- **implement-task.** Phase 4, the per-task loop including the review panel.

## The review panel

Code review is a standard stage of `implement-task`, not an optional side call, and is also invocable standalone.

- **The panel.** A roster of reviewers, each a dedicated `reviewer-<dimension>` subagent under `.claude/agents/reviewers/`, run in parallel, read-only, each obeying the no-assert-without-trace contract. The default roster is the nine dimensions in the profile: spec-conformance, correctness, state-and-concurrency, security-and-trust-boundary, failure-and-robustness, observability, test-adequacy, interface-and-data-integrity, conventions. Dimensions 3 to 6 map to the failure-pattern categories in the profile. Each reviewer writes its own file under `reviews/<task-id>/`, giving full visibility into raw findings.
- **The consolidator.** After the panel finishes, `review-consolidator` reads every reviewer's file, deduplicates overlapping findings, resolves disagreements between reviewers, re-validates each surviving finding against the actual code, ranks by severity (irreversibility times silence times blast radius), and writes `reviews/<task-id>/consolidated.md` as the authoritative verdict.
- **Mode.** A profile flag picks light mode (a subset of reviewers) or thorough mode (the full roster), because running nine reviewers plus a consolidator per task is expensive and not every task warrants it.
- **Pipeline position.** implement, then review panel, then consolidate, then walkthrough, then reconcile.

## Distribution and setup

No user-level install. Everything lives visibly inside the target repository, so the developer can read every agent, skill, command, script, and the full directory structure inside their own project before starting. Nothing is shared from the agentic-sdlc repository at runtime, and nothing hides in a user home directory.

Two steps.

### Step 1: Bootstrap

One command, run from the agentic-sdlc repository, with the target path as a parameter:

```
./install.sh /path/to/target-repo
```

`install.sh` copies `.claude/` from the agentic-sdlc repository into the target repository root. The `.claude/` directory carries everything Claude needs: `agents/`, `skills/`, `commands/`, `scripts/` (the Python CLIs the agents call), `config/` (the profile schema and examples), and `templates/` (the format templates placed into the artifact tree). A single copy brings the whole system across. This step is a plain copy and cannot be a skill inside the target, because nothing is in the target yet.

### Step 2: Discover and setup

1. Open Claude Code in the target repository, or restart the session if it was already open. Claude discovers agents, skills, and commands from the target's `.claude/` at session start. (A session restart is required for newly added agents and skills to register.)
2. Run the setup skill. It does two things at setup time, so the developer sees the full structure up front rather than lazily as agents run:
   - Creates the complete artifact tree via a Python CLI: every directory present, each with a README and the format template for its artifacts. Deterministic, idempotent, testable.
   - Produces `sdlc.config.yaml`: the greenfield interview, or the brownfield scan via `profile-discoverer`. The agent driving the skill decides what goes in the config and verifies the end state; the Python CLI guarantees the mechanical scaffolding is exact and repeatable.

The skill is the seam: the agent guarantees correctness end to end, while the CLI guarantees the scaffolding is exact every time. This is the CLI-tool-plus-skill pattern: deterministic work in a Python CLI, judgment in the skill.

### What lands in the target

```
target-repo/
  .claude/                  copied verbatim from agentic-sdlc
    agents/ skills/ commands/ scripts/ config/ templates/
  sdlc.config.yaml          generated by setup
  ai_docs/                  created by setup, fully documented, then filled by the phases
```

## The agentic-sdlc repository

The source of truth for the system.

```
agentic-sdlc/
  README.md
  CLAUDE.md
  DESIGN.md                 this document
  LICENSE
  install.sh                bootstrap, parameterised by target path
  .claude/                  everything copied into a target repo
    agents/
      profile-discoverer.md
      requirements-analyst.md
      architecture-advisor.md
      plan-decomposer.md
      feature-explorer.md
      task-preparer.md
      reviewers/                  nine reviewer agents, one per dimension
      review-consolidator.md
      code-walkthrough.md
      spec-reconciler.md
    skills/
      setup/SKILL.md
      sdlc/SKILL.md
      initialise-project/SKILL.md
      define-requirements/SKILL.md
      design-architecture/SKILL.md
      plan-implementation/SKILL.md
      implement-task/SKILL.md
    commands/
    scripts/
      scaffold.py
    config/
      sdlc.config.schema.yaml
      examples/
        python-aws.yaml
        typescript-node.yaml
        greenfield-minimal.yaml
    templates/
      charter.md prd.md architecture.md implementation-plan.md
      spec.md task-brief.md exploration.md review.md
      walkthrough.md reconciliation.md adr.md
      CONTEXT.md testing-conventions.md runbook.md
  docs/                     about the framework itself, not copied
    methodology.md
    getting-started.md
    phase-guides/
  ai_docs/                  optional, dogfood the pipeline on itself
```

## Conventions and constraints

- Python throughout. uv for running, Pydantic V2 for any models, type hints, British English. No Node. A Node CI gate is not carried over.
- `master` as the default branch name.
- No external trackers, no `gh` CLI, no synchronisation to any external system.
- No CI merge gate. Review is in-pipeline and on-demand, not a CI status check with waivers.
- Any structured output an agent must emit for downstream parsing uses XML with stable tags parsed by tolerant regex, never strict JSON. Most artifacts are markdown documents.

## Deliberately dropped

- The CI merge gate (the Node enforcement script, the GitHub workflow, the waiver-with-approver mechanism). Org-process machinery that presumes enforced pull-request status checks, premature for an ad-hoc spec-driven pipeline. The adversarial review method is kept; the gate is not.
- The external tracker sync.
- The epic and story hierarchy inside the pipeline. The unit is the flat task.
- An earlier scratchpad memory cache, token-conservation instructions, and anthropomorphic coaching. Replaced by real artifact files and modern tool use.
- A separate spec location and a mandatory subsystem index. Unified under one artifact root, subsystem index optional.

## Build sequence

1. The profile schema (`sdlc.config.schema.yaml`) and the scaffolding CLI (`scaffold.py`).
2. The generalised back half: `feature-explorer`, `task-preparer`, the `reviewers/` panel, `review-consolidator`, `code-walkthrough`, `spec-reconciler`, and the `implement-task` orchestration skill. The work here is decoupling plus adding the review panel.
3. The phase 3 join: `plan-implementation` and `plan-decomposer`, emitting spec documents and the task registry.
4. The front half: `initialise-project`, `define-requirements`, `design-architecture`, and their research subagents.
5. The setup skill, `install.sh`, and the brownfield `profile-discoverer`.
6. Documentation under `docs/`, and dogfooding the pipeline on the agentic-sdlc repository itself.
