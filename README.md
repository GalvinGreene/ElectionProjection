# Federal Election Projection Platform

A full-stack election analytics web app that:

- Ingests and normalizes polling data from multiple firms.
- Grades pollsters for historical bias and inaccuracy.
- Weights polls automatically based on recency, sample size, and grading.
- Tracks campaign finance records.
- Builds horse-race trend charts and win-probability projections.
- Produces a seat-balance semicircle chart with likelihood shading.
- Rebalances projections when redistricting maps change.

## 1) Features

### Poll ingestion and refresh
- Supports polling feeds via configurable adapters (CSV/API/HTML table sources).
- Runs scheduled updates (`python -m app.tasks.refresh_data`) to keep data current.
- Stores raw + normalized polls in SQLite.

### Pollster grading
- Computes:
  - **Mean Absolute Error (MAE)** by pollster over historical races.
  - **Directional bias** (average signed error by party/candidate).
  - **Reliability score** blended from sample count + error volatility.
- Produces a composite grade used by weighting.

### Projection engine
- Builds weighted vote share baselines per race.
- Simulates outcomes with Monte Carlo (default 20,000 draws).
- Outputs candidate win likelihood and race confidence buckets.

### Visualization
- Horse-race graphs for every race/candidate.
- Win probability cards.
- Semicircle seat chart with party color + opacity scaled by likelihood.

### Campaign finance
- Ingests campaign finance entries (adapter can be connected to official APIs/export files).
- Shows receipts/spending/cash-on-hand by candidate.

### Redistricting-aware seat model
- Stores district map versions and effective dates.
- Reprojects polling + prior vote baseline onto the active map.
- Automatically refreshes seat distribution when map changes.

## 2) Tech stack

- **Backend:** Flask, SQLAlchemy
- **Data processing:** pandas, numpy
- **Visualization:** Plotly
- **Scheduler:** APScheduler
- **Database:** SQLite (swap for Postgres in production)

## 3) Quick start

### Prerequisites
- Python 3.11+

### Install
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Initialize database
```bash
python -m app.tasks.init_db
```

### Load demo seed data
```bash
python -m app.tasks.seed_demo
```

### Run web app
```bash
python run.py
```

Open: `http://127.0.0.1:5000`

## 4) Operating guide

### Daily operation flow
1. Refresh polling + finance data:
   ```bash
   python -m app.tasks.refresh_data
   ```
2. Recompute pollster grades + projections:
   ```bash
   python -m app.tasks.recompute_models
   ```
3. (Optional) start scheduler for automated intervals:
   ```bash
   python -m app.tasks.scheduler
   ```

### Redistricting update flow
1. Add new map assignment file to `data/redistricting/*.csv`.
2. Ensure `effective_date` and district IDs are valid.
3. Run:
   ```bash
   python -m app.tasks.apply_redistricting
   python -m app.tasks.recompute_models
   ```

### Connecting real data sources
- Polling adapters: edit `app/services/polling_sources.py`
- Finance adapters: edit `app/services/finance_sources.py`
- Add source-specific normalization in `app/services/normalize.py`

## 5) Model notes

Weighted poll score:

`weight = recency_weight * sqrt(sample_size) * pollster_grade_weight`

Where:
- `recency_weight = exp(-days_old / half_life)`
- `pollster_grade_weight = 1 / (mae + bias_penalty + epsilon)`

Win likelihood is derived from simulated vote distributions and converted to percentages.

## 6) Production recommendations

- Move SQLite to Postgres.
- Add Redis + Celery for task queueing.
- Add API auth + rate limiting.
- Add robust scraper retry/backoff and anti-bot legal compliance checks.
- Add observability (Prometheus/Grafana).

## 7) Legal and data compliance

- Respect polling-firm Terms of Service and robots directives.
- Attribute source provenance for every poll and finance record.
- Verify campaign finance jurisdictions and filing cadence.
