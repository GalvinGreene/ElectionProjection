from apscheduler.schedulers.blocking import BlockingScheduler
from app.tasks.refresh_data import main as refresh_main
from app.tasks.recompute_models import main as recompute_main


def run_scheduler():
    scheduler = BlockingScheduler()
    scheduler.add_job(refresh_main, "interval", minutes=60)
    scheduler.add_job(recompute_main, "interval", minutes=60)
    print("Scheduler started. Refresh and model recompute every 60 minutes.")
    scheduler.start()


if __name__ == "__main__":
    run_scheduler()
