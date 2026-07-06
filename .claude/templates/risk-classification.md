<!-- TEMPLATE: the risk classification, written by the risk-classifier at
     ai_docs/initiatives/<initiative-id>/reviews/<task-id>/risk-classification.md.
     Risk is deliberately a separate judgement from magnitude: magnitude measures
     how much of the lifecycle the work needs, risk measures how dangerous the
     produced change is, and the two do not track each other, because a one-line
     change can be high risk and a large change can be routine. -->

<!-- PROVENANCE (append-only; only created is fixed) -->
created:        <ISO-8601 timestamp>
modified:       [<ISO-8601 timestamp>]
commits:        [<short-sha>]
agents:         [risk-classifier]
run-ids:        [<run-id>]
back-refs:      [<the diff or change reviewed>, <failure-pattern catalogue>]
forward-refs:   [reviews/<task-id>/]
<!-- END PROVENANCE -->

# Risk classification: <task-id>

## Risk tier

<low | medium | high>, because <one or two sentences naming the concrete
properties of the change that set the tier: paths touched, blast radius,
reversibility, matched failure patterns>.

## Failure patterns matched

| Pattern | Where the change touches it |
| --- | --- |
| <FP-id: pattern> | <file:line> |

<"None matched" when none.>

## Recommended reviewer subset

- <reviewer-dimension>: <one line: why this dimension earns a seat for this change>

## Dimensions deliberately left out

- <reviewer-dimension>: <one line: why this change does not need this dimension>
