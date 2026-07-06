# The data-engineering profile

This guide covers the four agent roles that distinguish the data-engineering profile from the neutral core: two grounding agents that pull external truth into artefacts, and two generators that consume those artefacts at the pipeline's one divergent stage. A project opts in by setting `schema_profile: data-engineering` in `sdlc.config.yaml` and recording the product locations the generators write to.

## Why grounding exists

Every subagent boots fresh and knows only its declared inputs, so a fact that never becomes an artefact never reaches a generating agent. The warehouse schema and the ADP Foundry operator contracts are exactly the knowledge whose absence produces the dbt model that compiles while joining on the wrong key. A grounding agent pulls each external source into a durable snapshot on the artefact bus, and a generation agent reads the snapshot there, never the live source. A snapshot rather than a live connection keeps generation auditable and repeatable: the exact schema a model was generated against is on the record, dated by its provenance header.

## The two grounding agents

- **schema-retrieval-warehouse** (`.claude/agents/data-engineering/schema-retrieval-warehouse.md`) queries the warehouse for the real tables, columns, and types the specs name, through the command-line route the project configures, and writes `ai_docs/reference/schema-snapshot.md`. When no route is configured yet, it accepts a hand-fed export and marks the snapshot hand-fed in its provenance. Staleness, not magnitude, drives a refresh. The command-line access route to the warehouse is the one critical-path external dependency of the profile, which is why it is requested in the first week of an implementation.
- **foundry-operator-reference** (`.claude/agents/data-engineering/foundry-operator-reference.md`) maintains `ai_docs/reference/operator-reference.md`, the mirrored reference of the ADP Foundry operator contracts: per operator, the full dotted import path, the parameter table, the return contract, one canonical usage block, and the rules the framework enforces. The mirror can lag the operator packages; that drift is a quality concern rather than a blocker, because a configuration generated against a stale contract fails the framework's own validation in the testing loop. The durable fix is making the framework source locally readable.

## The two generators

- **dbt-model-generator** (`.claude/agents/data-engineering/dbt-model-generator.md`) consumes the per-task spec and the schema snapshot and writes a dbt model plus its schema file to the dbt project location in `sdlc.config.yaml`. Every column comes from the snapshot; a column the snapshot does not carry is an escalation, never a guess. It follows the project's naming conventions (model name equal to the SQL filename, per-column descriptions, primary-key columns tested `not_null` and `unique`, sources referenced through `{{ source(...) }}`), and can emit an external-table source definition when the spec requires a new source.
- **adp-foundry-yaml-generator** (`.claude/agents/data-engineering/adp-foundry-yaml-generator.md`) consumes the per-task spec and the operator reference and writes a dag-factory DAG configuration to the Airflow location in `sdlc.config.yaml`: a unique DAG identifier, the default arguments, the audit callbacks, the ingestion or transformation task pattern, and environment values through variable templating rather than hardcoding. It references only operators and parameters the reference carries; an unknown operator need is an escalation, never an invention.

Both generators write the product into the application repository, never into the artefact tree, and both hand their artefact into the same shared downstream: risk classification, the review panel (including the guidelines reviewer), consolidation, walkthrough, and reconciliation.

## The capped testing loop

Each generator closes its stage by running the real validators, inside its own subagent context: run the Validation Commands the task's spec carries, parse the failures, fix each one, and re-run. For the dbt branch the validators are `dbt parse` and `dbt build --select <selector>` plus the spec's commands; for the Foundry branch they mirror the checks a CI pipeline runs on DAG YAML: the YAML parses, the DAG identifier is unique, the required fields are present (description, tags, both audit callbacks), and no environment value is hardcoded. The loop stops on exactly one of three conditions: zero failures (success), the three-iteration cap, or zero progress, and the remaining failures travel to the orchestrator in the completion summary. The cap and the zero-progress stop are what make the loop safe to run unattended.

## Bespoke grounding

The default convention follows the team's engineering guidelines: use the predefined ADP Foundry operators and the official warehouse schemas. A developer may add bespoke operators or a local schema snapshot under their own `ai_docs/data-engineering/` directory, for a new-provider integration or a local workflow. When a run uses that bespoke material, the orchestrator says so explicitly, in the conversation and in the run record, naming the default the run departed from, so the exception never becomes a silent norm.
