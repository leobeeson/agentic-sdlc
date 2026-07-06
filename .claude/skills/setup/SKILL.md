---
name: setup
description: |
  Sets up the agentic SDLC harness in this repository. Run once, immediately after
  install.sh has copied .claude/ in: generates sdlc.config.yaml (greenfield interview, or a
  brownfield survey the main agent performs itself), scaffolds the two-tier artefact tree,
  and generates the agent registry. The single setup entry point and the prerequisite for
  every run that follows.
scope: harness-core
phase: phase-1
---

# Setup

This skill installs the shared memory into the current repository and produces the one file that couples the harness to this project. It runs once, right after `install.sh` has copied `.claude/` in. Setup is harness, not a catalogue entry: it appears in no recipe and no registry, and every later run assumes setup has happened.

Setup does three things, in order:

1. Produce `sdlc.config.yaml` at the repository root: the single per-project profile, the whole of the per-project coupling.
2. Scaffold the two-tier artefact tree under the configured artefact root.
3. Generate the agent registry by scanning the agent manifests.

Setup does not produce the charter. The charter is the project-charter consultation's output; the profile is how the project is built, the charter is what and why.

## The pattern: a CLI for the mechanics, judgement in the conversation

The deterministic scaffolding is done by `.claude/scripts/scaffold.py`, run with `uv` (the script declares its dependencies inline). The judgement, which is the content of `sdlc.config.yaml`, is gathered in the conversation: by interview on a greenfield project, by your own survey on a brownfield one, confirmed by the developer either way.

## Step 1: Greenfield or brownfield

Scan quickly with Glob and Read: source files, a dependency manifest (`pyproject.toml`, `package.json`, a dbt project file), a DAG configuration directory, a test suite, CI configuration. Ignore `.claude/` itself. Meaningful source and configuration means brownfield; little more than the harness and a README means greenfield. State the assessment and let the developer confirm; the developer's answer is authoritative.

## Step 2: Gather the profile

The field set is `.claude/config/sdlc.config.schema.yaml`; worked examples sit in `.claude/config/examples/`. Gather every field, by the branch that applies.

### Greenfield: interview

Ask for the facts the profile needs, and nothing more:

- **project**: name, kind (data-engineering, application, library, tooling), stack, base branch.
- **artefact_tree.root**: default `ai_docs/`.
- **product_locations**: per generation target the project uses. For a data-engineering project: the directory the Airflow deployment scans for DAG YAML, the dbt project root, and the code root. The product lands where the deployment frameworks read, never in the artefact tree.
- **validation.commands**: the exact commands that prove a change, verbatim.
- **review**: the severity model (`three-tier` default) and the roster. Default to the nine core dimensions, adding `guidelines` when the project carries a guidelines mirror.
- **failure_patterns**: leave the default path; the catalogue accrues with use.
- **schema_profile**: `data-engineering` or `core`.
- **agents**: leave every role enabled unless the developer asks otherwise.

### Brownfield: survey the repository yourself

The survey is your own work inside this step; spawn nothing, persist no scan artefact, and let the survey's only output be the drafted `sdlc.config.yaml`. The repository is the only source of truth, in strict precedence: manifests, lockfiles, config files, CI workflows, and git metadata first; source read at a real file and line second; READMEs and prose last, as hints to chase to a concrete file. A wrong value asserted with false confidence is worse than an honest "could not determine".

Survey checklist:

- **Stack**: the dependency manifests and lockfiles name the language and package manager (`uv.lock` means uv, `pnpm-lock.yaml` means pnpm); version pins name the runtime. A dbt project file (`dbt_project.yml`) and a DAG configuration directory mark a data-engineering project.
- **Product locations**: the dbt project root; the directory the DAG loader scans (look for the dag-factory loader or the deployment workflow's sync path); the source root.
- **Validation commands**: the highest-value detection, because the testing loop runs these verbatim. Prefer the command CI actually runs (the workflow files), reconciled with manifest scripts and test configuration files.
- **Base branch**: `git symbolic-ref refs/remotes/origin/HEAD`; fall back to inspecting the branch list, and record any ambiguity.
- **Conventions**: the test layout and naming, the linter and type checker configs, the directory layout.

Draft `sdlc.config.yaml` from the survey, interview the developer only for what the survey could not determine, and walk the developer through the draft field by field, flagging every low-confidence inference. The developer confirms before the file is written.

## Step 3: Write and validate the profile

Write the confirmed values to `sdlc.config.yaml` at the repository root, leaving no placeholder behind. Then validate:

```
uv run .claude/scripts/scaffold.py validate --root .
```

Fix and re-run until the report is valid.

## Step 4: Scaffold the two-tier artefact tree

```
uv run .claude/scripts/scaffold.py init --root .
```

Idempotent; existing files are skipped, never overwritten. The command creates the artefact tree's two tiers under the configured root: the project spine (the charter, PRD, and architecture stubs, `reference/` with `CONTEXT.md`, `testing-conventions.md`, and `adrs/`, and `diagrams/`) and the initiatives tier (`initiatives/index.md`, the initiative registry with its focus note; one workspace per initiative is minted later, per intent, by the orchestrator via `scaffold.py new-initiative`). Read the JSON report and tell the developer what was created and what already existed.

## Step 5: Generate the agent registry

```
uv run .claude/scripts/generate_agent_registry.py --root .
```

The script scans the manifest frontmatter of every agent definition under `.claude/agents/` and every skill under `.claude/skills/`, and writes `ai_docs/agent-registry.md`: the catalogue of every agent role, what each consumes and produces, and whether each is core or profile scoped. The registry is never hand-edited; re-run the script whenever an agent role's file changes.

## Step 6: Report the final state

Tell the developer: the profile written and its key values; the tree created; the registry generated; and the next step, stating an intent in plain language (the intake skill takes it from there), or `/project-charter` to begin a new project explicitly.
