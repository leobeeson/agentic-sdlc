# Recipes and magnitude

This guide explains how a classified intent becomes the plan one run actually gets: the recipe library, the four pruning criteria, the mandatory stages, and the regenerate override, with worked compositions at three magnitudes.

## The recipe library

A recipe is a named, reusable stage sequence for one intent, meaning one target at one magnitude. The library lives under `.claude/config/recipes/`, one file per generation family (`dbt-model.yaml`, `adp-foundry-yaml.yaml`, `ad-hoc-code.yaml`) plus `non-generation.yaml` for the five targets that carry no magnitude. Each generation family holds five recipes, one per magnitude, produced by one table of inclusion conditions: every optional stage carries a condition, and the magnitude supplies the default answer. The orchestration skill reads these declarations; a recipe is never text inside a skill.

A recipe is rails with junctions, not a fixed list. The orchestrator selects the recipe keyed by the classified target and magnitude, or the nearest one when the pair sits between authored recipes, and when no recipe fits at all it falls back to dynamic decomposition, selecting and sequencing agent roles by their descriptions and contracts. An experienced developer may also name the stages directly, and the orchestrator composes the plan from that statement, subject only to the mandatory stages.

## The four pruning criteria

At composition time the orchestrator walks the recipe once and decides, stage by stage, what this run keeps. Every decision lands in the run record with a one-line rationale drawn from a fixed vocabulary.

- **Magnitude** (`pruned by magnitude`). The magnitude named the recipe; its remaining work is judgement at the margins. The orchestrator checks each optional stage's inclusion condition against the actual intent and departs from the default when the intent answers the condition differently. A new dbt model classified at `new-feature` normally omits the architecture stage, but when the request adds a data flow the project does not produce today, the intent changes the architectural design, and the architecture stage joins the plan.
- **Idempotency** (`skipped by idempotency`). An artefact that already exists at its deterministic path and validates against its template is reused, and the stage that would produce it is skipped.
- **Risk** (`selected by risk`). After generation, the risk-classifier reads the change just produced, sharpens its judgement with the failure-pattern catalogue, and recommends the reviewer subset. A low-risk change earns a small subset; a change on a security-sensitive path earns the full panel. Risk is deliberately separate from magnitude: a one-line change can be high risk and a large change can be routine.
- **The availability switch** (`disabled by configuration`). A project may disable an agent role in `sdlc.config.yaml`. A disabled role's stage is pruned before anything executes; a mandatory stage is immune, and when a disabled role's output is a required input of a later stage, the orchestrator asks the developer for the artefact directly rather than degrading silently.

## The mandatory stages

Three stages run in every composition that changes the product, and neither the magnitude defaults nor the availability switch can remove them: the review of the generated change together with its consolidation, the reconciliation check at each task boundary (a no-op when the task had no downstream impact), and the run record.

## The regenerate override

An existing valid artefact is normally reused. When the developer asks for an artefact to be rebuilt, the orchestrator treats the artefact as absent and runs the producing stage; the stage overwrites the file in place, and the provenance header appends a new modified entry, so lineage survives the rebuild.

## Three compositions of the dbt-model family

- **Bug fix.** The smallest composition: prepare the task, generate, classify the risk, review with the subset the risk recommends, consolidate, reconcile, record. The task-preparer builds the brief directly from the developer's request, which is the always-on specification layer: every generated change executes against a prepared specification, at every magnitude.
- **New feature.** Requirements join, the implementation plan joins and decomposes the work into tracked tasks, and each task runs explore, prepare, generate, classify risk, review, consolidate, walk through, reconcile. The architecture stage is in the composed plan only when the intent changes the architectural design, and even then an existing architecture document that already covers the change is reused rather than regenerated.
- **New project.** The full depth: charter, requirements, architecture and ADRs, implementation plan, then the per-task loop, with the review defaulting to the full panel. The grounding stage (the warehouse-schema retrieval) runs whenever the snapshot is missing or stale, at any point before generation, at every magnitude; staleness, not magnitude, drives it.

A developer who expected ten agent roles to run can read in the run record that six ran, which four did not, and why. That legibility is the run record's whole purpose.
