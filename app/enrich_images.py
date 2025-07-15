import os
import json
import psycopg2
from ultralytics import YOLO
from dotenv import load_dotenv
from datetime import datetime
from pathlib import Path
from PIL import Image

load_dotenv()

# Load YOLOv8 pretrained model
model = YOLO("yolov8n.pt")  # You can upgrade to yolov8m or yolov8x for better accuracy

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="db",  # use "localhost" if testing outside Docker
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD")
)
cur = conn.cursor()

# Create table
cur.execute("""
    CREATE SCHEMA IF NOT EXISTS raw;
    CREATE TABLE IF NOT EXISTS raw.image_detections (
        id SERIAL PRIMARY KEY,
        message_id BIGINT,
        image_path TEXT,
        object_class TEXT,
        confidence_score FLOAT
    );
""")

# Scan images
today = datetime.now().strftime("%Y-%m-%d")
image_root = f"data/raw/telegram_images/{today}"

for channel_dir in Path(image_root).glob("*"):
    for image_path in channel_dir.glob("*.jpg"):
        results = model(str(image_path))  # Run detection
        boxes = results[0].boxes

        # Extract message_id from filename (e.g., "123456.jpg")
        message_id = int(image_path.stem)

        for box in boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            class_name = model.names[cls]

            cur.execute("""
                INSERT INTO raw.image_detections (message_id, image_path, object_class, confidence_score)
                VALUES (%s, %s, %s, %s)
            """, (message_id, str(image_path), class_name, conf))

conn.commit()
cur.close()
conn.close()
print("Image enrichment complete.")
