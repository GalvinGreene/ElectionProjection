from app.db import SessionLocal
from app.models import HistoricalResult, DistrictMap


def main():
    session = SessionLocal()
    try:
        if session.query(HistoricalResult).count() == 0:
            session.add_all(
                [
                    HistoricalResult(pollster="Atlas Public Opinion", race_id="2024-US-HOUSE-VA-07", candidate="Candidate A", predicted_share=49.1, actual_share=48.3),
                    HistoricalResult(pollster="Atlas Public Opinion", race_id="2024-US-HOUSE-VA-07", candidate="Candidate B", predicted_share=46.2, actual_share=47.1),
                    HistoricalResult(pollster="National Pulse", race_id="2024-US-SENATE-AZ", candidate="Candidate C", predicted_share=46.9, actual_share=47.4),
                    HistoricalResult(pollster="National Pulse", race_id="2024-US-SENATE-AZ", candidate="Candidate D", predicted_share=48.0, actual_share=47.0),
                ]
            )
        if session.query(DistrictMap).count() == 0:
            session.add(DistrictMap(map_version="2026-cycle", district_id="VA-07", previous_district_id="VA-07", weight_transfer=1.0, effective_date=__import__("datetime").date(2026, 1, 1)))
        session.commit()
        print("Seed data loaded.")
    finally:
        session.close()


if __name__ == "__main__":
    main()
