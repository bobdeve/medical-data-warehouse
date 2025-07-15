from dagster import job, op

# Define an op for scraping Telegram data
@op
def scrape_telegram_data():
    # Logic for scraping Telegram data goes here
    print("Scraping Telegram data...")

# Define an op for loading raw data into Postgres
@op
def load_raw_to_postgres():
    # Logic to load raw data into Postgres goes here
    print("Loading raw data into Postgres...")

# Define an op to run DBT transformations
@op
def run_dbt_transformations():
    # Logic to run your DBT transformations goes here
    print("Running DBT transformations...")

# Define an op for running YOLO enrichment (image detection)
@op
def run_yolo_enrichment():
    # Logic for running YOLO image detection/enrichment goes here
    print("Running YOLO enrichment...")

# Define the job combining all the ops
@job
def telegram_data_pipeline():
    # The execution order:
    scrape_telegram_data()
    load_raw_to_postgres()
    run_dbt_transformations()
    run_yolo_enrichment()

from dagster import schedule

# Schedule to run the job every day at midnight
@schedule(cron_schedule="0 0 * * *", job=telegram_data_pipeline, execution_timezone="UTC")
def daily_telegram_pipeline_schedule():
    return {}
