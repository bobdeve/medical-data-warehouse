# Medical Data Warehouse Project

This project is a complete data pipeline and analytics platform designed to ingest, transform, and analyze Telegram message data and image detection results. It leverages modern tools including SQLAlchemy, FastAPI, dbt, and Dagster for orchestration to build a robust, observable, and schedulable data workflow.

---

## Table of Contents

- [Task 1: Data Modeling with SQLAlchemy](#task-1-data-modeling-with-sqlalchemy)
- [Task 2: Database Schema Correction and Migration](#task-2-database-schema-correction-and-migration)
- [Task 3: Data Transformation using dbt](#task-3-data-transformation-using-dbt)
- [Task 4: API Backend with FastAPI](#task-4-api-backend-with-fastapi)
- [Task 5: Pipeline Orchestration with Dagster](#task-5-pipeline-orchestration-with-dagster)
- [Running the Project](#running-the-project)
- [Environment Variables](#environment-variables)
- [Troubleshooting](#troubleshooting)
- [Contact](#contact)

---

## Task 1: Data Modeling with SQLAlchemy

### Objective
Define Python ORM classes that map to the underlying PostgreSQL database tables to enable easy querying and manipulation of Telegram messages and image detection data.

### What was done:
- Created `FctMessages` model to represent Telegram messages with columns:
  - `message_id` (primary key)
  - `channel_name` (indexed for faster lookup)
  - `post_text` (message content)
  - `post_date` (date of the post)
  - `channel_id` (foreign key to channel dimension, added later)
- Created `FctImageDetections` model to represent image detection results with:
  - `id` (primary key)
  - `message_id` (foreign key to message)
  - `object_class` (detected object category)
  - `object_label` (specific object label)
  - `confidence_score` (detection confidence as float)

### Why it matters:
- Using ORM models abstracts SQL queries and makes code more maintainable.
- Enables integration with FastAPI and other Python tools seamlessly.

---

## Task 2: Database Schema Correction and Migration

### Problem:
- The database was missing the `channel_id` column in the `fct_messages` table, which caused errors when querying.

### Steps to fix:
1. **Update the SQLAlchemy model** to include the missing `channel_id` column:
   ```python
   channel_id = Column(Integer)
Check your actual PostgreSQL database schema:

Use a database client (e.g., pgAdmin, DBeaver, or psql CLI) to verify columns in fct_messages.

Add the column to the database if missing:


ALTER TABLE fct_messages ADD COLUMN channel_id INTEGER;
Restart your API and re-run queries to confirm the error is resolved.

Why it matters:
ORM models must always match the underlying database schema.

Any schema mismatch causes runtime exceptions and API failures.

Task 3: Data Transformation using dbt
Objective
Create a data transformation layer that structures raw Telegram message data into a clean, analytics-ready fact table.

What was done:
Created a dbt SQL model fct_messages.sql that:

Extracts relevant fields (message_id, sender_id, message_text, etc.) from the raw staging table stg_telegram_messages.

Converts message timestamp to date format.

Joins with dim_channels and dim_dates dimension tables to enrich data with consistent IDs.

Calculates additional fields like message_length.

Sample SQL snippet:
sql
Copy
Edit
with base as (
    select
        msg.message_id,
        msg.sender_id,
        msg.message_text,
        msg.has_photo,
        msg.channel,
        msg.message_date::date as date
    from {{ ref('stg_telegram_messages') }} msg
),

joined as (
    select
        base.message_id,
        base.sender_id,
        base.message_text,
        base.has_photo,
        dc.channel_id,
        dd.date_id,
        length(base.message_text) as message_length
    from base
    left join {{ ref('dim_channels') }} dc on base.channel = dc.channel
    left join {{ ref('dim_dates') }} dd on base.date = dd.date
)

select * from joined
How to run dbt models:

dbt run --project-dir medical_dbt
Why it matters:
dbt handles SQL transformations in a modular, testable way.

Creates a centralized place for transformation logic, improving maintainability.

Task 4: API Backend with FastAPI
Objective
Build RESTful endpoints to interact with the data warehouse and serve insights.

Endpoints implemented:
Get Top Detected Objects:
GET /api/top-products
Returns the most frequently detected objects in images.

Get Channel Activity:
GET /api/channels/{channel_id}/activity
Returns statistics on message counts and post date ranges for a given channel.

Search Messages:
GET /api/messages/search?query=some_text
Returns messages matching the search query text.

Key backend components:
Used SQLAlchemy ORM sessions to query the database.

Handled filtering, grouping, and aggregation using SQLAlchemy functions (func.count(), func.min(), etc.).

Included error handling for missing data.

How to run API server:

uvicorn main:app --reload
Why it matters:
Provides real-time access to analytical data via HTTP.

Enables integration with frontends, dashboards, or other services.

Task 5: Pipeline Orchestration with Dagster
Objective
Move from ad-hoc scripts to a robust, observable, and schedulable data pipeline.

Steps performed:
Installed Dagster:


pip install dagster dagster-webserver
Defined Dagster Job and Ops:

Created Python functions (ops) for each pipeline step:

scrape_telegram_data - fetch raw messages.

load_raw_to_postgres - load scraped data to Postgres.

run_dbt_transformations - trigger dbt models to transform data.

run_yolo_enrichment - enrich messages with image detection results.

Composed these ops into a Dagster job.

Ran Dagster UI locally:


dagster dev -f path_to_pipeline.py
Accessed UI at http://127.0.0.1:3000 to inspect, trigger, and monitor runs.

Configured Scheduling:

Added schedules in Dagster to automate running jobs (e.g., daily).

Scheduling code uses Dagster’s @schedule decorator with cron or interval triggers.

Why it matters:
Orchestration ensures your data pipeline runs reliably on a schedule.

Provides visibility into pipeline execution, logs, and failures.

Supports scalability and maintainability for production workflows.

Running the Project
Prerequisites:
Python 3.8+

PostgreSQL database with necessary tables created

dbt installed and configured

Dagster installed

Steps:
Set environment variables (copy .env.example to .env and update):


TELE_API_ID=your_telegram_api_id
TELE_API_HASH=your_telegram_api_hash
TELE_PHONE_NUMBER=your_phone_number
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASS=your_db_password
DB_HOST=your_db_host
DB_PORT=your_db_port
Run database migrations and/or add missing columns as described in Task 2.

Run dbt transformations:


dbt run --project-dir medical_dbt
Start API backend:


uvicorn main:app --reload
Start Dagster UI and run the pipeline:

dagster dev -f path_to_pipeline.py
Open your browser at: http://127.0.0.1:3000

Monitor and schedule pipelines inside the Dagster UI.

Environment Variables
Variable	Description
TELE_API_ID	Telegram API ID
TELE_API_HASH	Telegram API Hash
TELE_PHONE_NUMBER	Phone number linked to Telegram
DB_NAME	Database name
DB_USER	Database user
DB_PASS	Database password
DB_HOST	Database host address
DB_PORT	Database port

Troubleshooting
SQLAlchemy attribute errors:
Check your ORM models and database schema for column mismatches.

UnicodeEncodeError writing SQL files:
Specify UTF-8 encoding when writing files in Python:


with open("file.sql", "w", encoding="utf-8") as f:
    f.write(sql_content)
Dagster errors about missing pyproject.toml config:
Use the -f flag with dagster dev to point to your pipeline Python file:











