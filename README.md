Interim Submission Report
Project Structure and Environment Setup
The project is organized into a reproducible structure managed through Git.

Environment dependencies are captured in requirements.txt.

Configuration and sensitive information are stored in a .env file, which is not committed to Git.

Optional Docker components (Dockerfile and docker-compose.yml) are included to ensure consistent deployment across different machines and environments.

This setup guarantees that anyone cloning the repo can replicate the exact environment and run the pipeline with minimal setup effort.

Raw Data Collection and Storage
Data is scraped from target Telegram channels using Telegram API.

Scraped raw data is saved as JSON files in a data lake folder structure partitioned by channel name and date to maintain organization and facilitate incremental updates.

Logging is implemented to monitor scraping progress and errors.

Errors are handled gracefully, with warnings logged without stopping the pipeline, ensuring reliability during long scraping sessions.

DBT Project Setup, Transformation, and Testing
A dbt project was initialized and configured to connect to the PostgreSQL database using a profiles.yml configuration file.

Raw JSON data is loaded into PostgreSQL into a dedicated raw schema.

Staging models (stg_telegram_messages) clean and lightly transform raw data by casting types and renaming columns.

Data mart models implement a star schema:

Dimension tables such as dim_channels and dim_dates.

Fact table fct_messages linking dimension keys and including key metrics.

Built-in dbt tests like unique and not_null ensure data quality on primary keys and critical columns.

Custom tests enforce business rules to maintain data integrity and trustworthiness.

Documentation and Repository Usability
The repository contains detailed setup instructions for environment preparation, scraping raw data, loading data, and running dbt models.

Usage examples include commands for running scraping (scrape.py), loading raw data (load_raw_data.py), and running dbt transformations (dbt run) and tests (dbt test).

Code and dbt models are documented with comments explaining their purpose and logic.

Visual diagrams (included in the docs/ folder) illustrate the overall data pipeline architecture and star schema for clarity.

This comprehensive documentation ensures any reviewer can replicate the full data pipeline manually and understand each component’s role.

