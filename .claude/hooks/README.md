# Lifecycle hooks

A lifecycle hook is a script Claude Code runs at a fixed event of the agent loop; the model neither invokes a hook nor can skip one. Hooks are one of the two deterministic enforcement surfaces of the harness, beside the permission policy in `.claude/settings.json`.

## What this starter ships

- `build_initiative_catalogue.py`, registered under `SessionStart` for `startup|clear|resume` (deliberately not on compaction, because the artefact-bus rebuild replaces compaction rather than complementing it). The hook reads the initiative registry and the run records, builds the initiative catalogue, and injects the catalogue plus the reconstitution protocol into the fresh session. Code with no judgement: every artefact read after the developer confirms an initiative belongs to the prime skill.

## What is deferred to implementation

The full deterministic gate surface is specified in the architecture document (chapter 6) and deliberately not implemented in this starter:

- The **permission policy**: allow and deny lists in `.claude/settings.json`, e.g. allow `dbt build`, `dbt test`, and read-only warehouse prefixes; deny destructive warehouse prefixes. The concrete patterns are an implementation decision, informed by a read-only survey of the team's current repository.
- The **pre-tool-use gate**: a `PreToolUse` hook that blocks a destructive warehouse statement hidden inside an allowed command, and enforces the reviewer write fence (the ten reviewers, the review-consolidator, the code-walkthrough, and the risk-classifier write only under their own output directories in the initiative workspace). In this starter the fence is stated as contract in each fenced agent's file; the hook is what makes the fence deterministic.
- The **post-tool-use observability hook**: records and never blocks, guarded so a logging failure never fails the work being logged.

The rule dividing the surfaces: a rule goes into a hook when code can decide it (a pattern, a path, a command prefix); a rule stays with an agent role when deciding needs judgement.
