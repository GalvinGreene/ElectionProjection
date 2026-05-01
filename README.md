# Federal Election Projection Platform (Simple Edition)

## One-command start

```bash
python start.py
```

This single command will:
1. Create `.venv`
2. Install dependencies
3. Initialize database
4. Seed baseline data
5. Refresh polls/finance
6. Recompute projections
7. Start web app at `http://127.0.0.1:5000`

## What you get

- Horse-race trend chart for active races
- Win probability projections
- Seat distribution chart
- House and Senate map views
- Campaign finance table
- Manual poll-entry form
- Background poll refresh button

## Background poll ingestion

Use the dashboard button **Run Poll Scrape in Background** to trigger ingestion without stopping the app.

## Keeping House district maps up to date

The app reads redistricting assignments from:

- `data/redistricting/*.csv`

CSV fields:
- `map_version`
- `district_id`
- `previous_district_id`
- `weight_transfer`
- `effective_date`

After adding/updating files, run:

```bash
.venv/bin/python -m app.tasks.apply_redistricting
.venv/bin/python -m app.tasks.recompute_models
```

## Manual run (if desired)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m app.tasks.init_db
python -m app.tasks.seed_demo
python -m app.tasks.refresh_data
python -m app.tasks.recompute_models
python run.py
```
