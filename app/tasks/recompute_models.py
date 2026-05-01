from app.db import SessionLocal
from app.models import HistoricalResult, PollsterGrade, Poll, RaceProjection
from app.services.modeling import compute_pollster_grade, weighted_projection, monte_carlo_win_probs


def main():
    session = SessionLocal()
    try:
        hist = session.query(HistoricalResult).all()
        grade_input = [
            {
                "pollster": h.pollster,
                "predicted_share": h.predicted_share,
                "actual_share": h.actual_share,
            }
            for h in hist
        ]
        grades = compute_pollster_grade(grade_input)

        session.query(PollsterGrade).delete()
        for pollster, metrics in grades.items():
            session.add(PollsterGrade(pollster=pollster, **metrics))

        grade_weights = {k: v["composite_weight"] for k, v in grades.items()}
        polls = session.query(Poll).all()
        poll_rows = [
            {
                "pollster": p.pollster,
                "race_id": p.race_id,
                "candidate": p.candidate,
                "party": p.party,
                "vote_share": p.vote_share,
                "sample_size": p.sample_size,
                "field_date": p.field_date,
            }
            for p in polls
        ]

        projection_by_race = weighted_projection(poll_rows, grade_weights)
        session.query(RaceProjection).delete()
        for race_id, rows in projection_by_race.items():
            for out in monte_carlo_win_probs(rows):
                session.add(RaceProjection(race_id=race_id, **out))

        session.commit()
        print("Pollster grades and projections recomputed.")
    finally:
        session.close()


if __name__ == "__main__":
    main()
