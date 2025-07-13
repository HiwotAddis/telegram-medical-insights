from telethon.sync import TelegramClient
from telethon.tl.types import MessageMediaPhoto
import os, json, datetime
from dotenv import load_dotenv
from app.logging_config import logger

load_dotenv()

api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")

client = TelegramClient('anon', api_id, api_hash)

async def scrape_channel(channel_username, max_messages=500):
    await client.start()
    logger.info(f"Scraping {channel_username}...")

    today = datetime.date.today().isoformat()
    messages = []
    image_dir = f"../data/raw/telegram_images/{today}/{channel_username}"
    os.makedirs(image_dir, exist_ok=True)

    try:
        async for msg in client.iter_messages(channel_username, limit=max_messages):
            if msg.text or msg.media:
                logger.info(f"Scraped message ID {msg.id}")
                msg_dict = msg.to_dict()
                messages.append(msg_dict)

                # Save image if exists
                if isinstance(msg.media, MessageMediaPhoto):
                    file_path = f"{image_dir}/{msg.id}.jpg"
                    await msg.download_media(file_path)
                    logger.info(f"Saved image: {file_path}")

        # Save messages if any
        if messages:
            json_path = f"../data/raw/telegram_messages/{today}/{channel_username}.json"
            os.makedirs(os.path.dirname(json_path), exist_ok=True)
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(messages, f, ensure_ascii=False, indent=2)
            logger.info(f"Saved {len(messages)} messages to {json_path}")
        else:
            logger.warning(f"No messages scraped from {channel_username}")

    except Exception as e:
        logger.error(f"Failed to scrape {channel_username}: {e}")
