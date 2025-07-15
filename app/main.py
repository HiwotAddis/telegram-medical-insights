import asyncio
from dotenv import load_dotenv
import os
from app.scraper import scrape_channel
from fastapi import FastAPI, Query, Path
from typing import List

from app.schemas import TopProduct, ChannelActivity, MessageSearchResult
from app.crud import get_top_products, get_channel_activity, search_messages

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
app = FastAPI(title="Telegram Medical Insights API")

@app.get("/api/reports/top-products", response_model=List[TopProduct])
def top_products(limit: int = Query(10, le=50)):
    return get_top_products(limit)

@app.get("/api/channels/{channel_name}/activity", response_model=List[ChannelActivity])
def channel_activity(channel_name: str = Path(...)):
    return get_channel_activity(channel_name)

@app.get("/api/search/messages", response_model=List[MessageSearchResult])
def search(query: str = Query(..., min_length=2)):
    return search_messages(query)