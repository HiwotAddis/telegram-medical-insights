import json
import os
import glob
import psycopg2
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host="db",  # or "localhost" if outside Docker
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD")
)

cur = conn.cursor()
cur.execute("""
    CREATE SCHEMA IF NOT EXISTS raw;
    CREATE TABLE IF NOT EXISTS raw.telegram_messages (
        id BIGINT PRIMARY KEY,
        message TEXT,
        date TIMESTAMP,
        sender_id BIGINT,
        channel TEXT,
        has_media BOOLEAN,
        raw_json JSONB
    );
""")

data_path = "data/raw/telegram_messages/*/*.json"
for file_path in glob.glob(data_path):
    channel = os.path.basename(file_path).replace(".json", "")
    with open(file_path) as f:
        messages = json.load(f)
        for msg in messages:
            cur.execute("""
                INSERT INTO raw.telegram_messages (id, message, date, sender_id, channel, has_media, raw_json)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING;
            """, (
                msg["id"],
                msg.get("message"),
                msg.get("date"),
                msg.get("from_id", {}).get("user_id"),
                channel,
                "media" in msg,
                json.dumps(msg)
            ))

conn.commit()
cur.close()
conn.close()
print("Raw data loaded to raw.telegram_messages")
