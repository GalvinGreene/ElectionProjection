import pandas as pd
from pathlib import Path
from app.db import SessionLocal
from app.models import DistrictMap


REDISTRICTING_DIR = Path("data/redistricting")


def main():
    session = SessionLocal()
    try:
        csvs = sorted(REDISTRICTING_DIR.glob("*.csv"))
        for csv_file in csvs:
            df = pd.read_csv(csv_file)
            for _, row in df.iterrows():
                session.add(
                    DistrictMap(
                        map_version=row["map_version"],
                        district_id=row["district_id"],
                        previous_district_id=row.get("previous_district_id", row["district_id"]),
                        weight_transfer=float(row.get("weight_transfer", 1.0)),
                        effective_date=row["effective_date"],
                    )
                )
        session.commit()
        print("Redistricting maps loaded.")
    finally:
        session.close()


if __name__ == "__main__":
    main()
