# Methodology

This document explains the conceptual model behind the agentic software development lifecycle framework: how it is structured, why it is structured that way, and what each part is for. It is the reasoning behind the system, not a how-to. The step-by-step instructions live in `getting-started.md` and the phase guides.

## The design thesis

One decision governs everything else. The framework ships as a project-agnostic spine, and every project-specific fact lives in a single per-project profile, `sdlc.config.yaml`. The spine is the set of agents, skills, commands, and scripts. The profile is one YAML file at the target repository root, generated once at setup and then read in slices by every agent that runs.

The spine never changes per project. There are no per-project edits to an agent, no forked skill, no patched script. A project differs from another project only in its profile. This is the line that makes the framework portable: the same spine drives a Python service, a TypeScript application, a greenfield prototype, or a brownfield codebase, because everything that varies has been pulled out of the spine and into the profile.

This matters for several concrete reasons.

- Portability. Copying the spine into a new repository and writing one profile is the whole setup. There is no surgery on the agents to teach them about the new project.
- A single source of coupling. Every project-specific fact lives in one file, so there is exactly one place to look when behaviour depends on the project, and exactly one place to change it.
- Safe upgrades. Because the spine is untouched per project, a newer version of the spine can be dropped into a repository without unpicking local modifications.
- Predictability. Two projects running the same spine version behave identically except where their profiles differ, which makes the framework's behaviour legible across projects.

The profile holds the tech stack, test commands, base branch, branch naming, conventions, the review roster and mode, failure-pattern idioms, and the artifact root. Hardcoded story prefixes, branch names, test commands, and audit paths are all gone from the spine; each is a profile field or is derived from the generated task registry. An agent that needs a project fact resolves its slice of the profile rather than carrying the fact in its own definition.

## The unit of work

The unit of work in the implementation phase is a flat task, identified by a single global sequence such as `TASK-001` and `TASK-002`. There is no epic or story hierarchy inside the pipeline. A task is the thing that flows through the whole implementation loop: explore, prepare, implement, review, walkthrough, reconcile.

Epic and story are product-planning vocabulary, and they belong to the requirements phase, where they help reason about scope and priority. They do not survive into the pipeline as structural levels, because a hierarchy of work items buys nothing once work is actually being built and adds coordination overhead at every stage. A flat sequence is simpler to track, simpler to address, and simpler to reason about.

Readability still matters, so tasks are grouped, but only for human reading. A spec document is a markdown file under `specs/`, one file per area of concern, named `specs/NN-<area>.md`, and it contains the tasks for that area. This grouping is file organisation and nothing more. It is not a formal hierarchy level, it does not change how a task is identified, and it does not change how a task flows through the loop. The grouping exists so a person can find related tasks together, not so the pipeline can reason about a tree.

## The phase model

The pipeline runs in phases, and the phases fall into two halves with deliberately different interaction models.

The front half is interactive. The skills converse with the developer to elicit and shape the early artifacts, they run in the main context, and they may spawn research subagents to fan out work and merge it back. This is judgment-heavy work where a person should be in the loop.

The back half is headless. An orchestration skill drives subagents that run in fresh context, report evidence, and never converse. This is execution-heavy work where the value comes from disciplined, repeatable, evidence-backed steps rather than conversation.

Before any phase runs, there is setup. Setup creates the complete artifact tree, with every directory documented, and writes the profile, either through a greenfield interview or a brownfield scan of the existing repository. Setup is run once. The profile it produces is how the project is built; everything that follows is what and why it is built.

The phases are as follows.

- Phase 0, charter. The `initialise-project` skill produces the charter: vision, objectives, success metrics, constraints, stakeholders, and risks. The profile already exists by this point because every agent, including this one, reads it.
- Phase 1, requirements. The `define-requirements` skill reads the charter and produces a requirements document with requirement identifiers, MoSCoW priority, user personas, and acceptance criteria in a Given/When/Then grammar. It may fan out requirements-analyst subagents for personas, functional requirements, and edge cases, then merge.
- Phase 2, architecture. The `design-architecture` skill reads the requirements and produces the architecture document, diagrams, seeds for the reference documents, and architectural decision records. It may spawn architecture-advisor subagents to weigh trade-offs in parallel.
- Phase 3, plan. The `plan-implementation` skill reads the architecture and the requirements and produces the implementation plan, the spec documents, and the task registry. It may spawn plan-decomposer subagents to break work into tasks and write the specs.
- Phase 4, implement. The `implement-task` orchestration skill runs the per-task loop, headless, once per task.

Phase 3 is the join. The front half is conversational planning; the back half is headless execution. Phase 3 sits between them and emits exactly what the implementation loop consumes: spec documents and a task registry. The implementation loop never had to author these before; it assumed they existed. Phase 3 is the phase that produces them, which is why it is the seam where the two halves meet.

## The implementation loop

Phase 4 runs a fixed loop per task. Each step has one job, writes one artifact, and hands a known input to the next step. The steps run in this order.

1. Explore. The feature-explorer reads the spec, the reference documents, the codebase, related repositories, and online documentation, and writes an exploration for the task. This is read-only investigation that establishes what exists and what the task must touch, before any code is written.
2. Prepare. The task-preparer reads the spec, the exploration, and the reference documents, and writes a task brief: the concrete, scoped plan for this one task. The mapping from task to spec is a lookup in the task registry, not a hardcoded rule.
3. Implement. The developer, working with Claude, writes the code and the tests. This is the only step that changes source code.
4. Review panel. The code-reviewer is spawned once per review dimension, in parallel, read-only, and each reviewer writes its own findings file under the task's review directory.
5. Consolidate. The review-consolidator reads every reviewer's file and writes the single authoritative consolidated verdict.
6. Walkthrough. The code-walkthrough reads the task brief, the exploration, the consolidated review, and the reference documents, and writes an execution-flow-ordered walkthrough for the developer to audit before merge.
7. Reconcile. The spec-reconciler takes the implementation as ground truth, updates the spec document in place so it reflects what was actually built, updates the reference documents and decision records, and writes a reconciliation report as the audit trail of what changed and why.

The loop is the same for every task, which is what makes it headless and repeatable. Each step's output is a durable artifact, so the state of a task is always inspectable, and a task can be picked up, reviewed, or re-run from its artifacts rather than from memory of a conversation.

## The review panel

The review panel is a standard stage of the implementation loop, not an optional side call, and it is also invocable on its own. Its design is the heart of the framework's quality model.

The panel is a roster of adversarial single-dimension reviewers. Each reviewer is a code-reviewer subagent spawned with exactly one dimension to scrutinise, run in parallel with the others, and read-only. One reviewer looks only at spec conformance, another only at correctness, another only at state and concurrency, and so on across the roster. Confining each reviewer to a single dimension keeps it sharp on that dimension and stops the diffusion of attention that happens when one reviewer is asked to judge everything at once. The default roster is nine dimensions:

- spec-conformance
- correctness
- state-and-concurrency
- security-and-trust-boundary
- failure-and-robustness
- observability
- test-adequacy
- interface-and-data-integrity
- conventions

Every reviewer obeys one hard rule: no assertion without a trace. A finding is not allowed unless it points to the actual file and line in the code or the deployed configuration. Code and deployed configuration are the only source of truth. The diff is the trigger and the prime suspect, but it is never the search boundary; a reviewer follows the behaviour into the rest of the codebase rather than stopping at the changed lines. This rule is what stops the panel from generating plausible-sounding but ungrounded objections.

Severity is not a feeling. It is computed as irreversibility times silence times blast radius.

- Irreversibility is how hard the damage is to undo once it happens.
- Silence is how quietly it fails, with a fault that fails loudly ranking below one that fails without any signal.
- Blast radius is how much of the system the fault can reach.

A fault that is irreversible, silent, and wide is the most severe; a fault that is easily undone, loud, and contained is the least. This model puts the focus on faults that are genuinely dangerous rather than on whichever issue is easiest to describe.

After the panel finishes, the review-consolidator turns the raw findings into one verdict. It does four things in sequence.

- Deduplicates findings that several reviewers raised about the same underlying issue.
- Resolves disagreements between reviewers rather than passing the conflict downstream.
- Re-validates each surviving finding against the actual code, to kill false positives before they reach the developer.
- Ranks the survivors by severity and writes the consolidated verdict.

Because every reviewer writes its own file and the consolidator writes a separate authoritative file, both the raw findings and the final verdict are visible. A profile flag selects light mode, a subset of reviewers, or thorough mode, the full roster, because running the whole panel plus a consolidator on every task is expensive and not every task warrants it.

## Living specs

The spec-reconciler updates the spec documents in place. After a task is implemented and reviewed, the reconciler takes the implementation as ground truth and rewrites the relevant spec so it reflects what was actually built, not just what was originally intended. The specs are living documents: at any point, a spec describes the current reality of the system.

This is safe precisely because there is no external tracker. In an earlier design the reconciler could only propose spec changes for a human to review, because a spec change had to be propagated by hand into separate external systems, and an automatic mutation would have desynchronised them. That constraint is gone. The spec is now a purely local file, the implementation is the source of truth, and the spec is mutated in place to match it. Every change the reconciler makes is recorded in a reconciliation report, so an in-place update remains fully reviewable after the fact.

## Self-containment

The framework is self-contained. There are no external trackers and no synchronisation to any outside system. The artifact tree under the configured artifact root is the system of record. Everything the pipeline produces lives there: the charter, the requirements, the architecture, the plan, the specs, the task briefs, the explorations, the reviews, the walkthroughs, the reconciliations, the reference documents, and the decision records.

Tracking lives inside the tree as files. The task registry, `specs/index.md`, is the single registry: it maps each task to its spec document and holds the status board for every task. It is the thing an external tracker would otherwise be, kept as a local file under version control alongside the code it describes. Because the registry and the artifacts are local files, the state of the project is always inspectable in the repository itself, with no dependency on any service.

## Lineage

The framework is not invented from nothing. It is a generalisation of mature, working bodies of work, recombined under the single design thesis.

- The back half, the implementation loop, is generalised from a mature implementation loop that already ran in production in another repository. The agents and the orchestration already worked; the work was decoupling them from one project's hardcoded assumptions, moving those assumptions into the profile, and adding the review panel between implement and walkthrough.
- The front half, the planning phases, is an upgrade of an earlier set of single-prompt planning consultants. Those were conversational prompts written for a weaker model: project initialisation, requirements, architecture, and implementation planning. Each is rebuilt as a modern agent or skill, with research subagents where fan-out helps, replacing scratchpad caches and token-conservation instructions with real artifact files and current tool use.
- The review panel generalises an adversarial readiness auditor. The auditor's no-assert-without-trace doctrine, its failure-pattern categories, and its severity reasoning become the shared reviewer contract and four of the roster dimensions, and its single-feature validator becomes the spec-conformance dimension. The standalone audit phase and its CI merge gate are dropped; the adversarial method is kept and folded into the loop.
