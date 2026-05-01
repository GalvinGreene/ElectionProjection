from flask import Flask, render_template
from sqlalchemy import select, func
from app.db import SessionLocal
from app.models import Poll, RaceProjection, FinanceRecord
import plotly.graph_objects as go

app = Flask(__name__)


def build_horse_race_chart(race_id: str, rows: list[Poll]):
    fig = go.Figure()
    by_candidate = {}
    for r in rows:
        by_candidate.setdefault(r.candidate, []).append(r)

    for candidate, c_rows in by_candidate.items():
        c_rows.sort(key=lambda x: x.field_date)
        fig.add_trace(
            go.Scatter(
                x=[i.field_date for i in c_rows],
                y=[i.vote_share for i in c_rows],
                mode="lines+markers",
                name=candidate,
            )
        )

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

        finance = (
            session.execute(
                select(
                    FinanceRecord.candidate,
                    FinanceRecord.party,
                    func.max(FinanceRecord.report_date),
                    func.max(FinanceRecord.receipts),
                    func.max(FinanceRecord.disbursements),
                    func.max(FinanceRecord.cash_on_hand),
                ).group_by(FinanceRecord.candidate, FinanceRecord.party)
            )
            .all()
        )

        return render_template("index.html", race_chart=race_chart, seat_chart=seat_chart, projections=projections, finance=finance)
    finally:
        session.close()
