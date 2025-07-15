from pydantic import BaseModel
from typing import List, Optional

class TopProduct(BaseModel):
    product: str
    count: int

class ChannelActivity(BaseModel):
    channel: str
    date: str
    message_count: int

class MessageSearchResult(BaseModel):
    message_id: int
    message: str
    date: str
    channel: str
