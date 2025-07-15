from dagster import repository
from pipeline import telegram_data_pipeline  # import your job

@repository
def my_repo():
    # Return a list of jobs (or ops, schedules, sensors, etc.)
    return [telegram_data_pipeline]
