# Value Realization Catalog

> A searchable, Snowflake-branded gallery of AI-extracted value stories across the SE portfolio.

A [Streamlit-in-Snowflake](https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit) application for the Snowflake AFE and Sales Engineering team.

## What It Does

Displays all value realization entries from `AFE.TEST.VALUE_REALIZATION_CATALOG` as a searchable, filterable card gallery. Each card shows capability chips, business challenge bullets, measured outcomes, and links to the rendered HTML slide. Built for SE field teams to quickly find relevant use cases before customer conversations.

## Business Value

| Benefit | Description |
|---------|-------------|
| Discovery speed | Find relevant use cases in seconds vs. searching Slack/emails |
| Consistency | All assets share Snowflake branding and structured format |
| Self-service | No RevOps or field-readiness ticket needed for use case assets |
| Growing library | Automatically updated as new repos are processed by the Ingestor |

## Architecture

| Component | Technology |
|-----------|------------|
| Frontend | Streamlit-in-Snowflake (dark Snowflake theme) |
| Data source | `AFE.TEST.VALUE_REALIZATION_CATALOG` |
| UI patterns | CSS card grid, capability chip tags, stat counters |
| Auth | Snowflake role-based access |

## Deployment

Deployed on Snowflake as: `SALES.SALES_ENGINEERING.VALUE_REALIZATION_CATALOG_APP`

```bash
snow streamlit deploy
```

## Local Development

```bash
uv sync
streamlit run streamlit_app.py
```

## Configuration

| Setting | Value |
|---------|-------|
| Warehouse | SNOWHOUSE |
| Runtime | SYSTEM$ST_CONTAINER_RUNTIME_PY3_11 |
| Compute Pool | STREAMLIT_DEDICATED_POOL_L |

## Related Projects

- [Value Realization Ingestor](https://github.com/sfc-gh-michael-lemke/value-realization-ingestor) — Populates the catalog from GitHub repos
- [Value Realization App](https://github.com/sfc-gh-michael-lemke/value-realization-app) — Generates use case assets from customer stories
- [value-realization-slide](https://github.com/sfc-gh-michael-lemke/value-realization-slide) — CoCo skill for generating individual slides

## Value Realization

The catalog closes the loop on the value realization pipeline: assets created by the Ingestor and App are surfaced here in a polished, searchable format. AEs and SEs can walk into customer conversations with relevant proof points at their fingertips — without asking RevOps, searching Confluence, or building slides from scratch.
