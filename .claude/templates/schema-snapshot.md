<!-- TEMPLATE: the warehouse-schema snapshot, written by the
     schema-retrieval-warehouse agent role at ai_docs/reference/schema-snapshot.md
     (the project spine). Project-wide data-engineering grounding: the real
     table and column names and types the dbt-model generator reads, so the
     generator never invents columns. A snapshot rather than a live connection
     keeps generation auditable and repeatable: the exact schema a model was
     generated against is on the record, dated by this header. A developer's
     bespoke snapshot for a new provider goes under their own
     ai_docs/data-engineering/ instead, and using it is stated explicitly. -->

<!-- PROVENANCE (append-only; only created is fixed) -->
created:        <ISO-8601 timestamp>
modified:       [<ISO-8601 timestamp>]
commits:        [<short-sha>]
agents:         [schema-retrieval-warehouse]
run-ids:        [<run-id>]
back-refs:      [<the warehouse queried, and the spec or request that named the target sources>]
forward-refs:   [<the specs and models generated against this snapshot>]
<!-- END PROVENANCE -->

# Warehouse-schema snapshot

- **Warehouse:** <the warehouse and account or environment queried>
- **Retrieved:** <ISO-8601 timestamp>
- **Access route:** <the command-line route used, e.g. the snowflake CLI, bq, or a hand-fed export; hand-fed grounding is flagged as such>
- **Covers:** <the schemas, tables, or datasets this snapshot covers, and why they were selected (the spec or request that named them)>

## <SCHEMA_NAME>.<TABLE_NAME>

<One sentence: what this table holds, from the warehouse comment or the team's knowledge; "no description recorded" when none.>

| Column | Type | Nullable | Description |
| --- | --- | --- | --- |
| <column_name> | <data type as the warehouse reports it> | <yes/no> | <from the warehouse comment; "none recorded" when none> |

**Row count at retrieval:** <count, or "not sampled">
**Freshness signal:** <last altered / last loaded timestamp the warehouse reports, when available>

## Staleness rule

This snapshot is stale when the target sources have changed since **Retrieved**
above, or when a spec names a source this snapshot does not cover. A stale or
missing snapshot re-runs the schema-retrieval-warehouse stage; nothing else
regenerates this file.
