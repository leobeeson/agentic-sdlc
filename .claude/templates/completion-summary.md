<!-- TEMPLATE: the fixed completion summary every subagent-realised agent role
     returns to the orchestrator as its final message. This is a message shape,
     not a file: the artefact carries the detail on the artefact bus, and the
     summary carries the control signal. Its content is set by one question:
     what must the orchestrator know right now, without reading the artefact, to
     continue the run safely. The summary is an extract of the artefact and
     never carries information the artefact does not hold. An empty section
     states "none" rather than disappearing, so absence is a statement and not
     an omission. Skill-realised agent roles return no summary: the main agent
     performed the work and already holds everything a summary would carry. -->

# <agent-role> completion, returned to the orchestrator

## Verdict
- <The agent role's status fields, its counts, and the path to the artefact it wrote.>

## Escalations: decisions with material impact that I did not make
- <Every question the agent role refused to settle by assumption. The rule is
  absolute: a question with material impact on the intent is never resolved by
  assuming an answer; the agent role completes what it can and raises the
  question here. Material impact is the bar: a summary that escalates trivia
  trains the orchestrator and the developer to ignore escalations. "None" when
  none.>

## Risks and inconsistencies: know now, detail in the artefact
- <What the orchestrator must know now even though the detail lives in the
  artefact, because the next stages build on it. "None" when none.>

## Read the full artefact before continuing: <yes | no>
