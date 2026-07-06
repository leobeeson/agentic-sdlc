<!-- TEMPLATE: the ADP Foundry operator reference, written by the
     foundry-operator-reference agent role at ai_docs/reference/operator-reference.md
     (the project spine). Project-wide data-engineering grounding: the mirrored
     reference of the operator and parameter contracts the ADP Foundry YAML
     generator grounds in, so the generator references real operators and
     supplies valid parameters. The mirror can lag the framework; that drift is
     a quality concern rather than a blocker, because a configuration generated
     against a stale contract fails the framework's own validation in the
     testing loop. The durable fix is making the framework source locally
     readable. -->

<!-- PROVENANCE (append-only; only created is fixed) -->
created:        <ISO-8601 timestamp>
modified:       [<ISO-8601 timestamp>]
commits:        [<short-sha>]
agents:         [foundry-operator-reference]
run-ids:        [<run-id>]
back-refs:      [<the mirrored operator documentation this reference was built from>]
forward-refs:   [<the ADP Foundry YAML configurations generated against this reference>]
<!-- END PROVENANCE -->

# ADP Foundry operator reference

- **Mirrored from:** <the operator documentation source and its version or date>
- **Drift risk:** this reference is a static mirror; when the operator packages change, this file lags until refreshed.

## <full.import.path.OperatorClassName>

<One or two sentences: what the operator does and when a pipeline uses it.>

**Parameters**

| Parameter | Type | Required | Meaning | Notes |
| --- | --- | --- | --- | --- |
| <name> | <type> | <yes/no> | <what the parameter controls> | <defaults, templating conventions, gotchas> |

**Return contract:** <what the operator pushes to XCom or returns, when downstream tasks depend on it>

**Canonical usage**

```yaml
<a minimal, valid task block using this operator, exactly as a DAG YAML would carry it>
```

**Rules the framework enforces:** <the conventions a configuration using this operator must satisfy, e.g. audit callbacks present, no hardcoded environment values, unique DAG identifier>

## Helper callables

| Callable | Import path | Used as | Purpose |
| --- | --- | --- | --- |
| <name> | <full.import.path> | <callback / branch / task> | <what it does> |
