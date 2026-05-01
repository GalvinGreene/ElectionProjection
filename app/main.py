from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import select, func
from app.db import SessionLocal
from app.models import Poll, RaceProjection, FinanceRecord
from app.tasks.refresh_data import main as refresh_task
import threading
import plotly.graph_objects as go

app = Flask(__name__)


def build_horse_race_chart(race_id: str, rows: list[Poll]):
    fig = go.Figure()
    by_candidate = {}
    for r in rows:
        by_candidate.setdefault(r.candidate, []).append(r)

    for candidate, c_rows in by_candidate.items():
        c_rows.sort(key=lambda x: x.field_date)
        fig.add_trace(go.Scatter(x=[i.field_date for i in c_rows], y=[i.vote_share for i in c_rows], mode="lines+markers", name=candidate))

    fig.update_layout(title=f"Horse Race Trend - {race_id}", xaxis_title="Date", yaxis_title="Vote Share %")
    return fig.to_html(full_html=False)


def build_seat_chart(projections):
    party_counts = {}
    for p in projections:
        party_counts[p.party] = party_counts.get(p.party, 0) + p.win_probability / 100.0

    labels, values, colors = [], [], []
    color_map = {"DEM": "rgba(0,82,204,0.8)", "REP": "rgba(204,39,54,0.8)", "IND": "rgba(128,128,128,0.8)"}
    for party, seats in sorted(party_counts.items()):
        labels.append(party)
        values.append(seats)
        colors.append(color_map.get(party, "rgba(120,120,120,0.8)"))

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.45, marker=dict(colors=colors), sort=False)])
    fig.update_layout(title="Projected Seat Balance (Likelihood-Weighted)")
    return fig.to_html(full_html=False)


def build_house_map(projections):
    by_race = {}
    for p in projections:
        if p.race_id.startswith("US-HOUSE"):
            by_race.setdefault(p.race_id, []).append(p)

    ids, values = [], []
    for race_id, rows in by_race.items():
        top = max(rows, key=lambda x: x.win_probability)
        ids.append(race_id)
        values.append(top.win_probability if top.party == "DEM" else -top.win_probability)

    fig = go.Figure(data=go.Bar(x=ids, y=values, marker_color=["#0052cc" if v >= 0 else "#cc2736" for v in values]))
    fig.update_layout(title="House District Lean Map (latest map version)", xaxis_title="District", yaxis_title="Lean (DEM + / REP -)")
    return fig.to_html(full_html=False)


def build_senate_map(projections):
    senate = [p for p in projections if p.race_id.startswith("US-SENATE")]
    fig = go.Figure(data=go.Scatter(x=[p.race_id for p in senate], y=[p.win_probability for p in senate], mode="markers", marker=dict(size=14, color=["#0052cc" if p.party == "DEM" else "#cc2736" for p in senate])))
    fig.update_layout(title="Senate Race Map (state race likelihood)", xaxis_title="State Race", yaxis_title="Win Probability %")
    return fig.to_html(full_html=False)


@app.post("/polls/add")
def add_poll():
    session = SessionLocal()
    try:
        poll = Poll(
            pollster=request.form["pollster"],
            race_id=request.form["race_id"],
            candidate=request.form["candidate"],
            party=request.form["party"],
            vote_share=float(request.form["vote_share"]),
            sample_size=int(request.form["sample_size"]),
            field_date=datetime.strptime(request.form["field_date"], "%Y-%m-%d").date(),
            source_url=request.form.get("source_url", "manual-entry"),
        )
        session.add(poll)
        session.commit()
    finally:
        session.close()
    return redirect(url_for("index"))


@app.post("/polls/background-refresh")
def refresh_background():
    threading.Thread(target=refresh_task, daemon=True).start()
    return redirect(url_for("index"))


@app.route("/")
def index():
    session = SessionLocal()
    try:
        races = session.execute(select(Poll.race_id).distinct()).scalars().all()
        selected_race = races[0] if races else None
        race_chart = None
        if selected_race:
            polls = session.execute(select(Poll).where(Poll.race_id == selected_race)).scalars().all()
            race_chart = build_horse_race_chart(selected_race, polls)

        projections = session.execute(select(RaceProjection)).scalars().all()
        seat_chart = build_seat_chart(projections) if projections else None
        house_map = build_house_map(projections) if projections else None
        senate_map = build_senate_map(projections) if projections else None

        finance = session.execute(select(FinanceRecord.candidate, FinanceRecord.party, func.max(FinanceRecord.report_date), func.max(FinanceRecord.receipts), func.max(FinanceRecord.disbursements), func.max(FinanceRecord.cash_on_hand)).group_by(FinanceRecord.candidate, FinanceRecord.party)).all()

        return render_template("index.html", race_chart=race_chart, seat_chart=seat_chart, house_map=house_map, senate_map=senate_map, projections=projections, finance=finance)
    finally:
        session.close()
