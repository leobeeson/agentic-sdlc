---
name: setup
description: |
  Sets up the agentic SDLC pipeline in this repository. Run once, immediately after the
  framework has been copied in, to scaffold the documented artifact tree and generate the
  per-project profile sdlc.config.yaml. Greenfield projects are set up by interview;
  brownfield projects are set up by scanning the existing codebase. This is the single
  setup entry point and the prerequisite for every phase that follows.
---

# Setup

This skill sets up the agentic SDLC pipeline inside the current repository. It runs once, right after `install.sh` has copied `.claude/` in, and it leaves the repository ready for phase 0.

You do two things, and only these two:

1. Create the complete, documented artifact tree under the configured `artifact_root`.
2. Produce `sdlc.config.yaml` at the repository root, the single source of every project-specific fact.

You do not produce the charter. The charter is phase 0, authored by the `initialise-project` skill. The profile is how the project is built; the charter is what and why it is built, and it comes later.

## The pattern: a CLI for the mechanics, you for the judgment

The deterministic scaffolding is done by a Python CLI, `.claude/scripts/scaffold.py`. It guarantees the tree is exact, complete, and repeatable. The judgment, which is the actual content of `sdlc.config.yaml`, is yours: you gather it by interview or by scan, you confirm it with the developer, and you verify the end state. You are the seam that guarantees correctness end to end; the CLI guarantees the scaffolding is exact every time.

Run `scaffold.py` with `uv`. The script declares its own dependencies inline, so `uv run` resolves them with no separate install step.

## Process

Work through these steps in order.

### Step 1: Scaffold the artifact tree

Run the init command from the repository root:

```
uv run .claude/scripts/scaffold.py init --root .
```

This is idempotent. It does the following:

- Creates every artifact directory under the configured `artifact_root` (default `ai_docs/`): `specs/`, `reference/`, `reference/adr/`, `diagrams/`, `task-briefs/`, `explorations/`, `reviews/`, `walkthroughs/`, `reconciliations/`.
- Places the singleton documents from the format templates: `specs/index.md` (the task registry), `reference/CONTEXT.md`, `reference/testing-conventions.md`, `runbook.md`, and the phase output stubs `charter.md`, `prd.md`, `architecture.md`, `implementation-plan.md`.
- Places a `README.md` in each artifact directory documenting that directory's purpose and the format of the artifacts it holds.
- Writes a starter `sdlc.config.yaml` skeleton at the repository root, with `TODO` placeholders for the values you fill in later steps.

Existing files are skipped, not overwritten. If you genuinely need to regenerate a file, pass `--force`. To target a non-default artifact root, pass `--artifact-root <name>`; otherwise the script reads the value from an existing config or falls back to `ai_docs`.

The command prints a JSON report with `created` and `skipped` lists. Read it and report to the developer what was created and what already existed.

### Step 2: Determine greenfield or brownfield

Decide whether this is a greenfield project (an empty or near-empty repository) or a brownfield project (an existing codebase with source, tests, and configuration already present).

- Run a quick scan with Glob and Read: look for source files, a build or dependency manifest (for example `pyproject.toml`, `package.json`, `go.mod`, `Cargo.toml`), a test suite, CI configuration, and deployment configuration. Ignore the `.claude/` framework and the freshly scaffolded `artifact_root`; they are present in both cases.
- If there is meaningful source code and project configuration, treat it as brownfield. If the repository holds little more than the framework and a readme, treat it as greenfield.
- State your assessment to the developer and confirm it before proceeding. The developer's answer is authoritative.

### Step 3: Gather the profile values

Take the branch that matches the project kind.

#### Greenfield: interview the developer

Ask the developer for the facts the profile needs, and nothing more. Cover:

- **Project**: name, a one or two sentence description, and the kind (`greenfield`).
- **Tech stack**: the primary language, the package manager, and the runtime version. Capture any further facts that help reviewers, for example frameworks, linter, type checker, under `tech_stack`; the schema permits extra fields.
- **Test gate**: the exact commands that run the test suite, and the test naming convention. The conventions document defaults to `reference/testing-conventions.md`.
- **Version control**: the default base branch that reviews and diffs compare against (default `master`).
- **Deploy surface**: whether the project has a deployment surface. If it does, set `deploy_config.detected` to true and record the deployment configuration file paths; if not, leave it as the default false with an empty list.
- **Review**: the review mode (`thorough` runs the full roster, `light` runs a subset) and the roster. Default to `thorough` with the full nine-dimension roster: spec-conformance, correctness, state-and-concurrency, security-and-trust-boundary, failure-and-robustness, observability, test-adequacy, interface-and-data-integrity, conventions.

Leave `task.id_scheme`, `task.spec_grouping`, `vcs.branch_scheme`, `reference` paths, `review.consolidator`, `review.severity_model`, `failure_patterns`, and `subsystem_index` at their skeleton defaults unless the developer asks to change them. `failure_patterns` start empty and accrue as the pipeline runs.

#### Brownfield: scan with the profile-discoverer agent

Spawn the `profile-discoverer` agent to scan the existing repository and draft `sdlc.config.yaml` from evidence: the language and package manager, the test runner and its invocation, CI files, deploy configuration, directory conventions, and recurring idioms. The agent returns a drafted profile grounded in what it actually found in the code.

Present that draft to the developer. Walk through each field, flag anything the agent inferred with low confidence, and ask the developer to confirm or correct. The developer's confirmation is authoritative; the scan is a strong starting point, not the final word.

### Step 4: Write the confirmed profile

Write the confirmed values into `sdlc.config.yaml` at the repository root, replacing every `TODO` placeholder left by the skeleton. Use `.claude/config/sdlc.config.schema.yaml` for the documented shape of each field and `.claude/config/examples/` for worked examples. Set `project.kind` to match the branch you took. Leave no `TODO` behind.

### Step 5: Validate

Run the validate command:

```
uv run .claude/scripts/scaffold.py validate --root .
```

It validates `sdlc.config.yaml` against the profile model and checks the artifact tree is complete, then prints a JSON report. If `valid` is true, continue. If not, read the `errors` and `missing_paths`, fix the cause (a malformed or incomplete config, or a missing tree path that a re-run of `init` will restore), and validate again. Repeat until it reports valid.

### Step 6: Report the final state

Tell the developer:

- The artifact tree that was created, under the configured `artifact_root`.
- The profile that was written, with the key values (project, tech stack, test gate, base branch, review mode and roster).
- That validation passed.
- The next step: run the `initialise-project` skill to begin phase 0 and author the charter.

## What the developer now has

After setup, everything lives visibly inside the developer's own repository, with full up-front visibility and nothing hidden in a user home directory:

- The whole `.claude/` framework: the agents, skills, commands, scripts, config schema, and templates.
- The complete, documented artifact tree under the configured `artifact_root`, every directory present with a README and the format template for its artifacts.
- `sdlc.config.yaml` at the repository root, the single source of project coupling that every agent reads thereafter.
