# Value Realization Catalog

> Self-service library of SE value stories — searchable, filterable, and slide-ready.

A [Streamlit-in-Snowflake](https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit) application for Snowflake Sales Engineering and RevOps teams.

## What It Does

Snowflake-branded SiS app that surfaces all entries in `AFE.TEST.VALUE_REALIZATION_CATALOG` as an interactive card gallery. Each card shows capability chips, business outcomes, and a rendered HTML slide. The catalog is searchable and filterable so field SEs can quickly locate relevant use cases by industry, capability, or keyword — and share them directly from the app.

## Business Value

| Benefit | Description |
|---------|-------------|
| Instant discovery | Find a relevant customer use case in seconds instead of hunting through shared drives |
| Always current | Catalog entries are live from Snowflake — new entries appear the moment they are ingested |
| Field-ready assets | Each entry includes a rendered HTML slide that can be shared directly in customer conversations |

## Architecture

| Component | Technology |
|-----------|------------|
| Frontend | Streamlit-in-Snowflake |
| Data source | `AFE.TEST.VALUE_REALIZATION_CATALOG` |
| AI/ML | N/A (AI runs at ingest time via Value Realization Ingestor) |
| Auth | Snowflake role-based access |

## Deployment

Deployed on Snowflake as: `SALES.SALES_ENGINEERING.VALUE_REALIZATION_CATALOG_APP`

### Deploy via Snowflake CLI

```bash
snow streamlit deploy
```

## Local Development

```bash
pip install -r requirements.txt  # or: uv sync
streamlit run streamlit_app.py
```

## Configuration

| Setting | Value |
|---------|-------|
| Warehouse | SNOWHOUSE |
| Runtime | SYSTEM$ST_CONTAINER_RUNTIME_PY3_11 |
| Compute Pool | STREAMLIT_DEDICATED_POOL |

## Value Realization

This catalog closes the loop on the value realization system: stories are created by the Value Realization App, ingested from GitHub by the Ingestor, and surfaced here for field consumption. It replaces informal tribal knowledge and scattered shared-drive assets with a structured, searchable library — turning the SE org's collective work into a compounding, reusable asset.
