import asyncio
from dotenv import load_dotenv
import os
from app.scraper import scrape_channel

load_dotenv()

channels = [
    "lobelia4cosmetics",
    "tikvahpharma",
    # Add more channels
]

async def main():
    for channel in channels:
        print(f"Scraping channel: {channel}")
        await scrape_channel(channel)

if __name__ == "__main__":
    asyncio.run(main())
