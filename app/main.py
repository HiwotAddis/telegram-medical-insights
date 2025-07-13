from dotenv import load_dotenv
import os

load_dotenv()

print("TELEGRAM_API_ID:", os.getenv("TELEGRAM_API_ID"))
print("Postgres DB:", os.getenv("POSTGRES_DB"))
