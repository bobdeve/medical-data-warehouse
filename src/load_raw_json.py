import os
import json
import psycopg2
from glob import glob
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASS,
    host=DB_HOST,
    port=DB_PORT
)
cursor = conn.cursor()

# Create raw table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS raw_telegram_messages (
    message_id BIGINT,
    date TIMESTAMP,
    sender_id TEXT,
    text TEXT,
    channel TEXT,
    has_photo BOOLEAN
);
""")
conn.commit()

# Find all JSON files in raw data path
json_files = glob('../data/raw/telegram_messages/*/*/messages.json')

for file in json_files:
    channel = file.split(os.sep)[-2]
    with open(file, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print(f"❌ Failed to parse {file}")
            continue

    for msg in data:
        try:
            msg_id = msg.get('id')
            msg_date = msg.get('date')
            # Convert ISO datetime string to Python datetime object
            if msg_date:
                msg_date = datetime.fromisoformat(msg_date.replace('Z', '+00:00'))

            sender = msg.get('from_id', {})
            sender_id = sender.get('user_id') if isinstance(sender, dict) else sender

            text = msg.get('message')
            has_photo = bool(msg.get('photo'))

            cursor.execute("""
                INSERT INTO raw_telegram_messages (
                    message_id, date, sender_id, text, channel, has_photo
                ) VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING;
            """, (msg_id, msg_date, sender_id, text, channel, has_photo))

        except Exception as e:
            print(f"⚠️ Skipping message due to error: {e}")
            continue

conn.commit()
cursor.close()
conn.close()

print("✅ All messages loaded into PostgreSQL.")
