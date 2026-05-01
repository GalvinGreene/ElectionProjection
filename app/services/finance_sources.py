from datetime import date


def fetch_finance_data():
    # Demo data. Connect to official campaign finance data source.
    return [
        {
            "candidate": "Candidate A",
            "party": "DEM",
            "receipts": 12_500_000,
            "disbursements": 9_300_000,
            "cash_on_hand": 3_200_000,
            "report_date": date.today(),
            "source_url": "https://example.com/finance/a",
        },
        {
            "candidate": "Candidate B",
            "party": "REP",
            "receipts": 11_100_000,
            "disbursements": 8_900_000,
            "cash_on_hand": 2_200_000,
            "report_date": date.today(),
            "source_url": "https://example.com/finance/b",
        },
    ]
