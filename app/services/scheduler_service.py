from apscheduler.schedulers.background import BackgroundScheduler

from app.services.reminder_service import (
    process_reminders
)

scheduler = BackgroundScheduler()


def start_scheduler():

    # 6 AM
    scheduler.add_job(
        process_reminders,
        trigger="cron",
        hour=6,
        minute=0
    )

    # 9 AM
    scheduler.add_job(
        process_reminders,
        trigger="cron",
        hour=9,
        minute=0
    )

    # 1 PM
    scheduler.add_job(
        process_reminders,
        trigger="cron",
        hour=13,
        minute=0
    )

    # 9 PM
    scheduler.add_job(
        process_reminders,
        trigger="cron",
        hour=21,
        minute=0
    )

    scheduler.start()

    print(
        "Scheduler Started Successfully"
    )