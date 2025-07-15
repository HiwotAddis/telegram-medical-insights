from dagster import ScheduleDefinition
from .jobs import full_pipeline

daily_schedule = ScheduleDefinition(
    job=full_pipeline,
    cron_schedule="0 6 * * *",  # Every day at 6:00 AM
    name="daily_telegram_pipeline"
)
