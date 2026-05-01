from app.db import SessionLocal
from app.models import Poll, FinanceRecord
from app.services.polling_sources import fetch_polling_data
from app.services.finance_sources import fetch_finance_data


def main():
    session = SessionLocal()
    try:
        for p in fetch_polling_data():
            session.add(Poll(**p))
        for f in fetch_finance_data():
            session.add(FinanceRecord(**f))
        session.commit()
        print("Polling and finance refreshed.")
    finally:
        session.close()


if __name__ == "__main__":
    main()
