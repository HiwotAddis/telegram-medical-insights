from dagster import op
import subprocess

@op
def scrape_telegram_data():
    subprocess.run(["python", "app/main.py"], check=True)

@op
def load_raw_to_postgres():
    subprocess.run(["python", "app/load_raw.py"], check=True)

@op
def run_dbt_transformations():
    subprocess.run(["dbt", "run", "--project-dir", "app/dbt"], check=True)

@op
def run_yolo_enrichment():
    subprocess.run(["python", "app/enrich_images.py"], check=True)
