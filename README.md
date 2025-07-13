This project is part of a larger data engineering challenge to build an end-to-end medical intelligence pipeline. It collects Telegram posts about medical products, stores the data in a structured warehouse (PostgreSQL), and uses dbt to build clean analytical models using a star schema. We also use YOLOv8 to enrich messages with visual object detection.

📁 Project Structure & Environment Setup
🔧 Reproducible Environment
The project uses a reproducible and production-ready layout:

bash
Copy
Edit
medical-data-warehouse/
├── data/                  # Raw images & scraped JSON files
├── notebooks/             # Jupyter notebooks for exploration and model dev
├── dbt/                   # DBT project with staging and mart models
├── docker-compose.yml     # Launches PostgreSQL + pgAdmin
├── Dockerfile             # Builds image with scraper + Python tools
├── requirements.txt       # Python packages
├── .env                   # Environment secrets (API keys, DB creds)
├── scrape.py              # Telegram scraping script
├── load.py                # Load raw JSON into PostgreSQL
├── detect.py              # YOLOv8 object detection on images
└── README.md
✅ Why this matters
Dockerized services ensure consistent deployment across dev/staging/prod.

.env decouples secrets from code.

Jupyter notebooks support visual debugging and step-by-step data flow tracking.

Anyone can reproduce this project by running just two commands:
docker-compose up and dbt run.

📨 Raw Data Collection and Storage
🔎 Scraping from Telegram
We used the telethon library to scrape public messages, images, and metadata from channels like:

CheMed123

Lobelia4Cosmetics

Each message is saved as a JSON file and image (if present).

🗂️ Raw Data Organization
kotlin
Copy
Edit
data/
└── raw/
    ├── CheMed123/
    │   ├── 2024-07-11.json
    │   └── ...
    ├── Lobelia4Cosmetics/
    │   └── 2024-07-11.json

data/
└── images/
    ├── CheMed123/
    └── Lobelia4Cosmetics/
🪵 Logging & Error Handling
Scraper logs all events using Python’s logging module.

Handles network errors, media download issues, and Telegram API limits gracefully.

✅ Best Practice: Raw data is organized by channel and date to support easy backfilling and partitioned processing.

🛠️ DBT Setup, Transformation & Testing
🔌 Connecting DBT to PostgreSQL
DBT is configured to transform raw Telegram data into clean models.

Raw Layer: Raw JSON is loaded into a raw_messages table.

Staging Layer: stg_messages.sql cleans the raw schema and casts types.

Mart Layer: fct_messages.sql, dim_channels.sql, dim_dates.sql implement a star schema for analysis.

⭐ Star Schema Overview
markdown
Copy
Edit
dim_channels    dim_dates
     │              │
     └────┐    ┌────┘
          ▼    ▼
       fct_messages
fct_messages: central fact table with post text, date, image presence.

dim_channels: metadata for each Telegram channel.

dim_dates: time dimension for aggregation.

✅ DBT Tests
unique + not_null for primary keys.

Referential integrity for foreign keys (channel_id, date_key).

Configured via schema.yml.

yaml
Copy
Edit
  - name: message_id
    tests:
      - not_null
      - unique
✅ Result: Clean, trustworthy, and queryable data warehouse.

🧠 Optional Enrichment: YOLOv8 Object Detection
As an additional enrichment step:

We used the Ultralytics YOLOv8 model to detect objects in images.

Detected labels: "person", "bottle", "banana", etc.

Detection results are stored in fct_image_detections with:

message_id (FK to fct_messages)

object_class

object_label

confidence_score

✅ This adds image intelligence to text-based messages and allows tracking of common medical products visually.

🖥️ Repository Usability & Reproducibility
🔄 Step-by-Step Usage
Clone the repo and install dependencies:

bash
Copy
Edit
git clone https://github.com/yourusername/medical-data-warehouse.git
cd medical-data-warehouse
pip install -r requirements.txt
Configure .env with:

Telegram API credentials

PostgreSQL DB credentials

Launch services:

bash
Copy
Edit
docker-compose up
Run scrapers and loaders:

bash
Copy
Edit
python scrape.py
python load.py
dbt run
Optional: Run YOLO detection:

bash
Copy
Edit
python detect.py
📸 Visuals
📊 Star Schema

🔁 Pipeline Flow
text
Copy
Edit
[ Telegram API ]
      ↓
[ JSON & Image Storage ]
      ↓
[ PostgreSQL Raw Layer ]
      ↓
[ DBT Staging → Mart ]
      ↓
[ YOLOv8 Image Enrichment ]
✅ Submission Alignment
Metric	Status
Project environment & reproducibility	✅
Raw data lake setup + logging	✅
DBT transformation & star schema	✅
DBT tests for validation	✅
Engineering justifications (README + report)	✅
Visual diagrams (schema + pipeline)	✅
Clear setup instructions in README	✅

📌 Future Enhancements
Deploy YOLOv8 detection as a microservice with queue-based inference.

Use Apache Airflow to schedule scraping and loading pipelines.

Add Looker Studio or Metabase dashboards on top of marts.

Store enriched detections in a vector store for advanced search.
