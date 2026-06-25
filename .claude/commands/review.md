---
description: Run the review panel and consolidator standalone for a task or change.
argument-hint: <task-id>
---

Run the review panel for task $ARGUMENTS using the `implement-task` skill's review stage: spawn one `reviewer-<dimension>` agent per dimension in `review.roster` (in parallel), then run `review-consolidator` to produce the authoritative consolidated verdict at `<artifact_root>/reviews/$ARGUMENTS/consolidated.md`.
