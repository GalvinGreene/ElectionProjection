"""Polling source adapters.
Replace stubs with real API/scraper implementations for each polling firm.
"""

from datetime import date, timedelta


def fetch_polling_data():
    # Demo data. Replace with source-specific parsers.
    today = date.today()
    return [
        {
            "pollster": "Atlas Public Opinion",
            "race_id": "US-HOUSE-VA-07",
            "candidate": "Candidate A",
            "party": "DEM",
            "vote_share": 48.2,
            "sample_size": 950,
            "field_date": today - timedelta(days=1),
            "source_url": "https://example.com/polls/atlas",
        },
        {
            "pollster": "Atlas Public Opinion",
            "race_id": "US-HOUSE-VA-07",
            "candidate": "Candidate B",
            "party": "REP",
            "vote_share": 46.9,
            "sample_size": 950,
            "field_date": today - timedelta(days=1),
            "source_url": "https://example.com/polls/atlas",
        },
        {
            "pollster": "National Pulse",
            "race_id": "US-SENATE-AZ",
            "candidate": "Candidate C",
            "party": "DEM",
            "vote_share": 47.0,
            "sample_size": 1200,
            "field_date": today - timedelta(days=2),
            "source_url": "https://example.com/polls/pulse",
        },
        {
            "pollster": "National Pulse",
            "race_id": "US-SENATE-AZ",
            "candidate": "Candidate D",
            "party": "REP",
            "vote_share": 47.5,
            "sample_size": 1200,
            "field_date": today - timedelta(days=2),
            "source_url": "https://example.com/polls/pulse",
        },
    ]
